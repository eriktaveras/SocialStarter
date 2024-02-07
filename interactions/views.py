from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Like, Post
from django.shortcuts import render, redirect
from .models import Comment, Post
from .forms import CommentForm 
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Intenta eliminar el "me gusta" si ya existe; de lo contrario, crea uno nuevo.
    like_exists = Like.objects.filter(user=request.user, post=post).exists()
    
    if like_exists:
        Like.objects.filter(user=request.user, post=post).delete()
    else:
        Like.objects.create(user=request.user, post=post)

    # Intenta redirigir al usuario a la página anterior de forma segura.
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url:
        return HttpResponseRedirect(referer_url)
    else:
        # En caso de que HTTP_REFERER no esté disponible, redirige a una ubicación segura como el feed.
        return HttpResponseRedirect(reverse('feed'))


@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('/')
    else:
        form = CommentForm()
    return render(request, 'interactions/comment_form.html', {'form': form})