from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True) 
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique_for_date='created_at', editable=False)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug and self.text:
            self.slug = slugify(self.text[:50])
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.created_at.year, self.created_at.month, self.created_at.day, self.slug])

    def __str__(self):
        return f"{self.user.username}'s post at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

