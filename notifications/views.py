from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@login_required
def notification_list(request):
    """Vista para mostrar todas las notificaciones del usuario"""
    notifications = request.user.notifications.all()
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications
    })

@login_required
def get_notifications(request):
    """API para obtener notificaciones no leídas"""
    notifications = request.user.notifications.filter(is_read=False)
    
    # Formato para respuesta JSON
    notification_data = []
    for notification in notifications:
        notification_data.append({
            'id': notification.id,
            'sender': notification.sender.username,
            'sender_avatar': notification.sender.profile.avatar_url if hasattr(notification.sender, 'profile') else None,
            'text': notification.text,
            'type': notification.notification_type,
            'url': notification.url,
            'created_at': notification.created_at.strftime('%b %d, %Y, %I:%M %p'),
            'is_read': notification.is_read
        })
    
    return JsonResponse({
        'count': len(notification_data),
        'notifications': notification_data
    })

@login_required
def mark_as_read(request, notification_id=None):
    """Marcar notificaciones como leídas"""
    if notification_id:
        # Marcar una notificación específica como leída
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
    else:
        # Marcar todas las notificaciones como leídas
        request.user.notifications.filter(is_read=False).update(is_read=True)
    
    # Redireccionar según el contexto
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('notifications:notification_list')

def create_notification(sender, recipient, notification_type, text, url="", object_id=None):
    """Utilidad para crear notificaciones desde cualquier parte de la aplicación"""
    # No crear notificaciones para uno mismo
    if sender == recipient:
        return None
        
    notification = Notification.objects.create(
        sender=sender,
        recipient=recipient,
        notification_type=notification_type,
        text=text,
        url=url,
        object_id=object_id
    )
    
    # Send WebSocket notification
    channel_layer = get_channel_layer()
    notification_data = {
        'id': notification.id,
        'sender': notification.sender.username,
        'sender_avatar': notification.sender.profile.avatar_url if hasattr(notification.sender, 'profile') else None,
        'text': notification.text,
        'type': notification.notification_type,
        'url': notification.url,
        'created_at': notification.created_at.strftime('%b %d, %Y, %I:%M %p'),
        'is_read': notification.is_read
    }
    
    async_to_sync(channel_layer.group_send)(
        f'notifications_{recipient.id}',
        {
            'type': 'notification_message',
            'notification': notification_data,
            'count': Notification.objects.filter(recipient=recipient, is_read=False).count()
        }
    )
    
    return notification 