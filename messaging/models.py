from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q

class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation {self.id} between {', '.join(user.username for user in self.participants.all())}"

    @property
    def last_message(self):
        return self.messages.order_by('-created_at').first()
    
    @staticmethod
    def get_or_create_conversation(user1, user2):
        """Get or create a conversation between two users"""
        # Find if a conversation already exists between these users
        conversations = Conversation.objects.filter(participants=user1).filter(participants=user2)
        
        if conversations.exists():
            return conversations.first()
        else:
            # Create a new conversation
            conversation = Conversation.objects.create()
            conversation.participants.add(user1, user2)
            return conversation


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
