from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post
from django.http import JsonResponse
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

@login_required
def feed(request):
    # Get all posts ordered by creation date, from newest to oldest
    posts = Post.objects.all().order_by('-created_at')
    
    # Pagination
    posts_per_page = 5  # Number of posts per page
    posts_page_1 = posts[:posts_per_page]
    has_more = posts.count() > posts_per_page
    
    return render(request, 'feed/feed.html', {
        'posts': posts_page_1,
        'has_more': has_more
    })

@login_required
def load_more(request):
    # Don't strictly check for XMLHttpRequest to be more flexible
    # if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
    #     return JsonResponse({'error': 'Invalid request'}, status=400)
    
    # Log the request for debugging
    logger.info(f"Load more request received - GET params: {request.GET}")
    
    # Get page number from request (default to 1)
    page = int(request.GET.get('page', 1))
    posts_per_page = 5  # Same as in the feed view
    
    # Calculate start and end indices
    start = (page - 1) * posts_per_page
    end = page * posts_per_page
    
    # Log calculation details
    logger.info(f"Fetching posts from {start} to {end}")
    
    # Get posts for the requested page
    posts = Post.objects.all().order_by('-created_at')[start:end]
    
    # Check if there are more posts
    total_posts = Post.objects.count()
    has_more = total_posts > end
    
    # Log the number of posts fetched
    logger.info(f"Fetched {posts.count()} posts, has_more: {has_more}")
    
    # Render posts to HTML
    html = render_to_string('feed/partials/post_list.html', {'posts': posts}, request=request)
    
    return JsonResponse({
        'html': html,
        'has_more': has_more
    })
