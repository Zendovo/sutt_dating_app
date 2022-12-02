from django.db import models
from user.models import ChatRequest, UserProfile

# Create your models here.
class ChatMessages(models.Model):
    chat = models.ForeignKey(ChatRequest, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

