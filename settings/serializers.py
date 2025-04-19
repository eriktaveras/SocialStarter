from rest_framework import serializers
from .models import UserSetting

class UserSettingSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserSetting
        fields = [
            'id', 'user', 'user_username', 'theme', 'language', 
            'privacy_level', 'email_notifications', 'push_notifications',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
        
    def validate(self, data):
        """
        Validate user settings data.
        """
        return data 