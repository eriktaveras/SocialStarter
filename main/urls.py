from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('posts/', include(('posts.urls', 'posts'), namespace='posts')),  
    path('relationship/', include(('relationship.urls', 'relationship'), namespace='relationship')),
    path('', include(('feed.urls', 'feed'), namespace='feed')),
    path('interactions/', include(('interactions.urls', 'interactions'), namespace='interactions')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('messages/', include(('messaging.urls', 'messaging'), namespace='messaging')),
    path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
    path('settings/', include(('settings.urls', 'settings'), namespace='settings')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
