from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post

@login_required
def feed(request):
    # Obtener todos los posts ordenados por fecha de creación, de los más recientes a los más antiguos
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'feed/feed.html', {'posts': posts})
