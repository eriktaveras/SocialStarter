# users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from relationship.models import Relationship
from django.shortcuts import get_object_or_404
from users.models import User
from django.contrib import messages
from posts.models import Post
from interactions.views import get_liked_posts

def view_profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    is_following = False
    friend_request_sent = False
    friend_request_received = False
    
    if request.user.is_authenticated:
        is_following = Relationship.objects.filter(follower=request.user, following=user_profile, is_accepted=True).exists()
        friend_request_sent = Relationship.objects.filter(follower=request.user, following=user_profile, is_accepted=False).exists()
        friend_request_received = Relationship.objects.filter(follower=user_profile, following=request.user, is_accepted=False).exists()

    # Get the user's posts ordered by creation date
    posts = user_profile.posts.all().order_by('-created_at')

    # Get liked posts for the "likes" tab
    liked_posts = get_liked_posts(request, username)

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'is_following': is_following,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
        'liked_posts': liked_posts,
    }
    return render(request, 'users/profile.html', context)

def connections(request, username):
    """View to display a user's followers and following"""
    user_profile = get_object_or_404(User, username=username)
    
    # Determine which tab to show (followers or following)
    active_tab = request.GET.get('tab', 'followers')
    
    # Get followers - users who follow the profile user
    followers = [rel.follower for rel in Relationship.objects.filter(
        following=user_profile,
        is_accepted=True
    )]
    
    # Get following - users who the profile user follows
    followings = [rel.following for rel in Relationship.objects.filter(
        follower=user_profile,
        is_accepted=True
    )]
    
    context = {
        'user_profile': user_profile,
        'followers': followers,
        'followings': followings,
        'active_tab': active_tab,
    }
    
    return render(request, 'users/connections.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('users:view_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'form': form})