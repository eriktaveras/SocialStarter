# users/urls.py

from django.urls import path
from .views import view_profile, edit_profile

urlpatterns = [
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<str:username>/', view_profile, name='view_profile'),
]
