# views.py
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Post
from .forms import PostForm

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts/post_list.html'
    ordering = ['-created_at']

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/crear_post.html'
    success_url = reverse_lazy('feed:feed')  
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
