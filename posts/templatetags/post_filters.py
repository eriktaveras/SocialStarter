from django import template

register = template.Library()

@register.filter(name='is_liked')
def is_liked(post, user):
    return post.likes.filter(id=user.id).exists()
