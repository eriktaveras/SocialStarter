# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from relationship.models import Relationship
from django.shortcuts import get_object_or_404
from users.models import User

def view_profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    is_following = Relationship.objects.filter(follower=request.user, following=user_profile, is_accepted=True).exists()
    friend_request_sent = Relationship.objects.filter(follower=request.user, following=user_profile, is_accepted=False).exists()
    friend_request_received = Relationship.objects.filter(follower=user_profile, following=request.user, is_accepted=False).exists()

    # Obtener las publicaciones del usuario del perfil
    posts = user_profile.posts.all().order_by('-created_at')

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'is_following': is_following,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('users:view_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'form': form})