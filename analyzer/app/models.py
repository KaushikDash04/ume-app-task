from django.db import models
import json

class QueryLog(models.Model):
    query = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tone = models.CharField(max_length=50)
    intent = models.CharField(max_length=50)
    suggested_actions = models.JSONField()

    def __str__(self):
        return self.query

    class Meta:
        db_table = "app_querylog"
