from django.contrib import admin
from .models import Like, Comment

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')  
    search_fields = ('user__username', 'post__id') 

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'text', 'created_at')
    search_fields = ('user__username', 'post__id', 'text')
    list_filter = ('created_at',) 
    ordering = ('-created_at',) 
    
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
