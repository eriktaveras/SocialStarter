from django import forms
from .models import UserSetting


class UserSettingForm(forms.ModelForm):
    """Form for handling user settings"""
    
    class Meta:
        model = UserSetting
        fields = ['theme', 'language', 'email_notifications', 'push_notifications', 'privacy_level']
        
        widgets = {
            'theme': forms.Select(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'push_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privacy_level': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add any custom initialization here if needed
        self.fields['email_notifications'].help_text = 'Receive email notifications for important updates'
        self.fields['push_notifications'].help_text = 'Receive push notifications on your device' 