from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image', 'video']  
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border border-gray-300 rounded-md', 
                'placeholder': 'Escribe algo...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
            }),
            'video': forms.FileInput(attrs={
                'class': 'bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
            }),
        }
        labels = {
            'text': 'Texto',
            'image': 'Imagen',
            'video': 'Video',
        }
