from django import template

register = template.Library()

@register.filter(name='exclude_user')
def exclude_user(queryset, user):
    """Exclude a user from a queryset and return the first item."""
    if not queryset:
        return None
    other_users = queryset.exclude(id=user.id)
    if other_users.exists():
        return other_users.first()
    return None 