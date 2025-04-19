from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import os

def user_avatar_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/avatars/<filename>
    return f'user_{instance.user.id}/avatars/{filename}'

def user_cover_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/covers/<filename>
    return f'user_{instance.user.id}/covers/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    cover_image = models.ImageField(upload_to=user_cover_path, blank=True, null=True)

    def __str__(self):
        return self.user.username
        
    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            # Return a default avatar
            return f"{settings.STATIC_URL}img/default-avatar.png"
            
    @property
    def cover_url(self):
        if self.cover_image and hasattr(self.cover_image, 'url'):
            return self.cover_image.url
        return None

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
