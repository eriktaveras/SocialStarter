# urls.py
from django.urls import path
from .views import PostListView, PostCreateView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('crear/', PostCreateView.as_view(), name='crear_post'),
]
