from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Max, Count
from django.http import JsonResponse
from .models import Conversation, Message
from .forms import MessageForm

@login_required
def inbox(request):
    """View to display the user's conversations"""
    # Get all conversations where the user is a participant
    conversations = request.user.conversations.all().annotate(
        latest_message_time=Max('messages__created_at'),
        unread_count=Count('messages', filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user))
    ).order_by('-latest_message_time')
    
    return render(request, 'messaging/inbox.html', {
        'conversations': conversations
    })

@login_required
def conversation_detail(request, conversation_id):
    """View a conversation and send messages"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    # Mark all unread messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    # Get the other participant
    other_user = conversation.participants.exclude(id=request.user.id).first()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            # Update conversation timestamp
            conversation.save()  # This updates the updated_at field
            
            # If it's an AJAX request, return a JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': {
                        'content': message.content,
                        'sender_id': message.sender.id,
                        'created_at': message.created_at.strftime('%b %d, %Y, %I:%M %p'),
                    }
                })
            
            return redirect('messaging:conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    # Get messages for this conversation
    messages = conversation.messages.order_by('created_at')
    
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'form': form,
        'messages': messages,
        'other_user': other_user
    })

@login_required
def start_conversation(request, username):
    """Start a new conversation with a user"""
    other_user = get_object_or_404(User, username=username)
    
    if other_user == request.user:
        # Can't start a conversation with yourself
        return redirect('messaging:inbox')
    
    # Get or create a conversation between these users
    conversation = Conversation.get_or_create_conversation(request.user, other_user)
    
    return redirect('messaging:conversation_detail', conversation_id=conversation.id)

@login_required
def load_more_messages(request, conversation_id):
    """Load more messages for infinite scrolling"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    # Get the offset (how many messages are already loaded)
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))
    
    # Get messages with pagination
    messages = conversation.messages.order_by('-created_at')[offset:offset+limit]
    
    # Format for JSON response
    messages_data = []
    for message in messages:
        messages_data.append({
            'id': message.id,
            'content': message.content,
            'sender_id': message.sender.id,
            'sender_username': message.sender.username,
            'created_at': message.created_at.strftime('%b %d, %Y, %I:%M %p'),
            'is_read': message.is_read
        })
    
    return JsonResponse({
        'messages': messages_data,
        'has_more': conversation.messages.count() > offset + limit
    })
