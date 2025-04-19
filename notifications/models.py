from django.db import models
from django.conf import settings

class Notification(models.Model):
    # Tipos de notificaciones
    LIKE = 'like'
    COMMENT = 'comment'
    FOLLOW = 'follow'
    MESSAGE = 'message'
    
    NOTIFICATION_TYPES = (
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        (FOLLOW, 'Follow'),
        (MESSAGE, 'Message'),
    )
    
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    # ID del objeto relacionado (post_id, comment_id, etc.)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    # Texto de la notificación
    text = models.CharField(max_length=255)
    # URL donde dirigir al hacer clic en la notificación
    url = models.CharField(max_length=255, blank=True)
    # Si la notificación ha sido leída
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification to {self.recipient.username} from {self.sender.username}: {self.text}" 