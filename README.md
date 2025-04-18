# ume-app-task

## Setup
1. Create and activate virtual environment
2. Install requirements: `pip install -r requirements.txt`
3. Create `.env` file with `OPENAI_API_KEY` 
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## API Endpoint
- POST `/api/analyze/`
- Request: `{"query": "your text here"}`
- Response: Includes analysis and suggested actions

## Testing
Use Postman or curl:
```bash
curl -X POST http://localhost:8000/api/analyze/ \
-H "Content-Type: application/json" \
-d '{"query": "I need help"}'


## Sample Query & Response

{
    "query": "Where can I book a cab to the airport?"
}

{
    "query": "Where can I book a cab to the airport?",
    "analysis": {
        "tone": "neutral",
        "intent": "QUESTION"
    },
    "suggested_actions": [
        {
            "action_code": "ACTION_001",
            "display_text": "Ask Help"
        },
        {
            "action_code": "ACTION_002",
            "display_text": "Search FAQ"
        },
        {
            "action_code": "ACTION_003",
            "display_text": "Contact Support"
        }
    ]
}



{ "query": "Can someone help me reset my password?" }
{
    "query": "Can someone help me reset my password?",
    "analysis": {
        "tone": "neutral",
        "intent": "SUPPORT"
    },
    "suggested_actions": [
        {
            "action_code": "ACTION_001",
            "display_text": "Reset Password"
        },
        {
            "action_code": "ACTION_002",
            "display_text": "Contact Support"
        },
        {
            "action_code": "ACTION_003",
            "display_text": "Check Help Center"
        }
    ]
}






{
    "query": "I want to order pizza."
}

{
    "query": "I want to order pizza.",
    "analysis": {
        "tone": "happy",
        "intent": "ORDER"
    },
    "suggested_actions": [
        {
            "action_code": "ACTION_001",
            "display_text": "Order Food Online"
        },
        {
            "action_code": "ACTION_002",
            "display_text": "Find Recipes"
        },
        {
            "action_code": "ACTION_003",
            "display_text": "Contact Restaurant"
        }
    ]
}



