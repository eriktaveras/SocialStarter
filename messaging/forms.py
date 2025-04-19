from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    """Form for sending a message"""
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full bg-dark-light rounded-lg border-0 p-3 focus:ring-2 focus:ring-primary focus:outline-none',
            'placeholder': 'Type your message...',
            'rows': 3
        }),
        label=''
    )

    class Meta:
        model = Message
        fields = ['content'] 