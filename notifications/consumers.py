import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        # Reject the connection if the user is not authenticated
        if not self.user.is_authenticated:
            await self.close()
            return
            
        # Each user gets their own notification group
        self.notification_group_name = f"notifications_{self.user.id}"
        
        # Join room group
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial notification count on connection
        count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            "type": "notification_count",
            "count": count
        }))
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket (from client)
    async def receive(self, text_data):
        text_data_json = json.dumps(text_data)
        message_type = text_data_json.get('type', '')
        
        if message_type == 'mark_as_read':
            notification_id = text_data_json.get('notification_id')
            if notification_id:
                await self.mark_notification_as_read(notification_id)
            else:
                await self.mark_all_as_read()
                
            # Send updated count
            count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                "type": "notification_count",
                "count": count
            }))
    
    # Receive message from room group
    async def notification_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
        
    @sync_to_async
    def get_unread_count(self):
        return Notification.objects.filter(recipient=self.user, is_read=False).count()
    
    @sync_to_async
    def mark_notification_as_read(self, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, recipient=self.user)
            notification.is_read = True
            notification.save()
            return True
        except Notification.DoesNotExist:
            return False
    
    @sync_to_async
    def mark_all_as_read(self):
        Notification.objects.filter(recipient=self.user, is_read=False).update(is_read=True)
        return True 