from django.urls import path
from .views import feed  # Ajusta este importe según dónde esté definida tu vista

urlpatterns = [
    path('', feed, name='feed'),
]
