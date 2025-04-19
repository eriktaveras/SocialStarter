from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'settings'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'api/settings', views.UserSettingViewSet, basename='user-settings')

urlpatterns = [
    path('profile/', views.profile_settings, name='profile'),
    path('account/', views.account_settings, name='account'),
    path('privacy/', views.privacy_settings, name='privacy'),
    path('notifications/', views.notification_settings, name='notifications'),
    # Default redirect to profile settings
    path('', views.profile_settings, name='index'),
    # Include the router URLs
    path('', include(router.urls)),
] 