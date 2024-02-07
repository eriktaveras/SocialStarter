from django.urls import path
from .views import follow_user, send_friend_request, accept_friend_request

urlpatterns = [
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('send-friend-request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:relationship_id>/', accept_friend_request, name='accept_friend_request'),
]
