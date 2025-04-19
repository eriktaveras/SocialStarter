from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('api/get/', views.get_notifications, name='get_notifications'),
    path('mark-as-read/', views.mark_as_read, name='mark_all_as_read'),
    path('mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
] 