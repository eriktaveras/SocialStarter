from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Relationship
from django.contrib.auth.decorators import login_required

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if Relationship.objects.filter(follower=request.user, following=user_to_follow).exists():
        pass
    else:
        Relationship(follower=request.user, following=user_to_follow, is_accepted=True).save()
    return redirect('/')


@login_required
def send_friend_request(request, user_id):
    user_to_friend = get_object_or_404(User, id=user_id)
    if Relationship.objects.filter(follower=request.user, following=user_to_friend).exists():
        pass
    else:
        Relationship(follower=request.user, following=user_to_friend).save() 
    return redirect('/')


@login_required
def accept_friend_request(request, relationship_id):
    relationship = get_object_or_404(Relationship, id=relationship_id, following=request.user, is_accepted=False)
    relationship.is_accepted = True
    relationship.save()
    return redirect('alguna-vista')
