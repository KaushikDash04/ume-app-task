import os
import json
import requests
from dotenv import load_dotenv
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import QueryLog
from .serializers import QueryLogSerializer

load_dotenv()

class AnalyzeView(APIView):
    def post(self, request):
        query = request.data.get("query", "").strip()
        if not query:
            return Response({"error": "Query is required."}, status=status.HTTP_400_BAD_REQUEST)
        if len(query) > 1000:
            return Response({"error": "Query too long (max 1000 characters)."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tone, intent = self.call_llm_api(query)
            suggested_actions = self.suggest_actions(tone, intent)
            
            log_entry = QueryLog.objects.create(
                query=query,
                tone=tone,
                intent=intent,
                suggested_actions=json.dumps(suggested_actions),
            )
            
            return Response({
                "query": query,
                "analysis": {
                    "tone": tone,
                    "intent": intent,
                },
                "suggested_actions": suggested_actions,
            })
            
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return Response(
                {"error": "Unable to process your request. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def call_llm_api(self, query):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("OPENAI_API_KEY not configured")
            return "neutral", "UNKNOWN"

        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            messages = [
                {
                    "role": "system",
                    "content": (
                        "Analyze the user's message and respond with JSON containing: "
                        "1. 'tone' (happy, sad, angry, neutral, urgent, etc.) "
                        "2. 'intent' (ORDER, CANCEL, QUESTION, SUPPORT, COMPLAINT, FEEDBACK, GREETING, or UNKNOWN)"
                    )
                },
                {"role": "user", "content": query}
            ]

            data = {
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "response_format": {"type": "json_object"},
                "max_tokens": 150,
                "temperature": 0.3,
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=10
            )
            response.raise_for_status()
            
            response_data = response.json()
            generated_text = response_data["choices"][0]["message"]["content"]
            parsed = json.loads(generated_text)
            
            tone = parsed.get("tone", "neutral").lower()
            intent = parsed.get("intent", "UNKNOWN").upper()
            
            return tone, intent

        except Exception as e:
            print(f"LLM API error: {str(e)}")
            return "neutral", "UNKNOWN"

    def suggest_actions(self, tone, intent):
        actions = {
            "ORDER": ["Order Food Online", "Find Recipes", "Contact Restaurant"],
            "CANCEL": ["Cancel Order", "Contact Support", "Request Refund"],
            "QUESTION": ["Ask Help", "Search FAQ", "Contact Support"],
            "GREETING": ["Say Hello", "Start Conversation"],
            "SUPPORT": ["Reset Password", "Contact Support", "Check Help Center"],
            "COMPLAINT": ["File Complaint", "Request Callback", "Contact Manager"],
            "FEEDBACK": ["Submit Feedback", "Rate Service", "Suggest Improvement"],
            "UNKNOWN": ["Contact Support", "Browse Help Center", "Try Rephrasing"]
        }

        suggestions = actions.get(intent, actions["UNKNOWN"])
        return [
            {"action_code": f"ACTION_{i+1:03d}", "display_text": action}
            for i, action in enumerate(suggestions[:3])
        ]