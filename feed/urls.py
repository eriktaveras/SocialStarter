from django.urls import path
from .views import feed, load_more

urlpatterns = [
    path('', feed, name='feed'),
    path('load-more/', load_more, name='load_more'),
]
