from django.contrib import admin
from .models import UserSetting


@admin.register(UserSetting)
class UserSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'language', 'privacy_level', 'email_notifications', 'push_notifications', 'updated_at')
    list_filter = ('theme', 'language', 'privacy_level', 'email_notifications', 'push_notifications')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Appearance', {
            'fields': ('theme', 'language')
        }),
        ('Notifications', {
            'fields': ('email_notifications', 'push_notifications')
        }),
        ('Privacy', {
            'fields': ('privacy_level',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    ) 