from django.urls import path
from .views import like_post, comment_post

urlpatterns = [
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('comment/<int:post_id>/', comment_post, name='comment_post'),
]
