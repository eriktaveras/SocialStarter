from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Like, Post
from django.shortcuts import render, redirect
from .models import Comment, Post
from .forms import CommentForm 
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.loader import render_to_string

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if request is AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # Try to delete the like if it exists; otherwise, create a new one
    like_exists = Like.objects.filter(user=request.user, post=post).exists()
    
    if like_exists:
        Like.objects.filter(user=request.user, post=post).delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True
    
    # Return JSON response if AJAX request
    if is_ajax:
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': post.likes.count()
        })
    
    # Otherwise, redirect back to the referring page
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url:
        return HttpResponseRedirect(referer_url)
    else:
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


def get_liked_posts(request, username):
    """Get all posts liked by a specific user."""
    user = get_object_or_404(User, username=username)
    
    # Get all posts that the user has liked
    liked_posts = Post.objects.filter(likes__user=user).order_by('-likes__created_at')
    
    return liked_posts

@login_required
def ajax_load_liked_posts(request, username):
    """Load liked posts via AJAX for the profile page."""
    user = get_object_or_404(User, username=username)
    
    # Get all posts that the user has liked
    liked_posts = Post.objects.filter(likes__user=user).order_by('-likes__created_at')
    
    # Render the liked posts to HTML
    html = render_to_string('interactions/liked_posts.html', {
        'liked_posts': liked_posts,
        'request': request,  # Pass request to template for request.user checks
    })
    
    return JsonResponse({
        'html': html
    })