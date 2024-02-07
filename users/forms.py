# En forms.py dentro de tu app (puedes crear este archivo si no existe)

from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from .models import Profile

class CustomSignupForm(SignupForm):
    username = forms.CharField(max_length=30, label='Username')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.username = self.cleaned_data['username']
        user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Cuenta algo sobre ti...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border-gray-300 rounded-md',
                'placeholder': 'Tu ubicación'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border-gray-300 rounded-md',
                'type': 'date'
            }),
        }