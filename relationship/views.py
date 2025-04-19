from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Relationship
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def follow_user(request, user_id):
    """
    Handle both follow and unfollow actions
    If a relationship already exists, it will be deleted (unfollow)
    If it doesn't exist, it will be created (follow)
    """
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # Don't allow self-follow
    if request.user.id == user_id:
        messages.error(request, "You cannot follow yourself.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # Check if already following
    relationship = Relationship.objects.filter(
        follower=request.user, 
        following=user_to_follow
    ).first()
    
    if relationship:
        # Unfollow - delete the relationship
        relationship.delete()
        messages.success(request, f"You have unfollowed {user_to_follow.username}.")
    else:
        # Follow - create the relationship
        Relationship.objects.create(
            follower=request.user, 
            following=user_to_follow, 
            is_accepted=True
        )
        messages.success(request, f"You are now following {user_to_follow.username}.")
    
    # Redirect back to the previous page or to the user's profile
    next_url = request.META.get('HTTP_REFERER')
    if not next_url:
        next_url = reverse('users:view_profile', kwargs={'username': user_to_follow.username})
    
    return HttpResponseRedirect(next_url)


@login_required
def send_friend_request(request, user_id):
    user_to_friend = get_object_or_404(User, id=user_id)
    
    # Don't allow self-friend requests
    if request.user.id == user_id:
        messages.error(request, "You cannot send a friend request to yourself.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    # Check if request already exists
    existing_request = Relationship.objects.filter(
        follower=request.user, 
        following=user_to_friend,
        is_accepted=False
    ).exists()
    
    # Check if already friends
    already_friends = Relationship.objects.filter(
        follower=request.user, 
        following=user_to_friend,
        is_accepted=True
    ).exists()
    
    if already_friends:
        messages.info(request, f"You are already friends with {user_to_friend.username}.")
    elif existing_request:
        messages.info(request, f"You have already sent a friend request to {user_to_friend.username}.")
    else:
        Relationship.objects.create(
            follower=request.user, 
            following=user_to_friend,
            is_accepted=False
        )
        messages.success(request, f"Friend request sent to {user_to_friend.username}.")
    
    # Redirect back to the previous page or to the user's profile
    next_url = request.META.get('HTTP_REFERER')
    if not next_url:
        next_url = reverse('users:view_profile', kwargs={'username': user_to_friend.username})
    
    return HttpResponseRedirect(next_url)


@login_required
def accept_friend_request(request, relationship_id):
    relationship = get_object_or_404(
        Relationship, 
        id=relationship_id, 
        following=request.user, 
        is_accepted=False
    )
    
    relationship.is_accepted = True
    relationship.save()
    
    # Create the reciprocal relationship
    Relationship.objects.get_or_create(
        follower=request.user,
        following=relationship.follower,
        defaults={'is_accepted': True}
    )
    
    messages.success(request, f"You are now friends with {relationship.follower.username}.")
    
    # Redirect back to the previous page or to notifications
    next_url = request.META.get('HTTP_REFERER')
    if not next_url:
        next_url = '/'  # Default to home page
    
    return HttpResponseRedirect(next_url)
