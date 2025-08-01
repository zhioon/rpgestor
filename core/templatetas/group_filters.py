from django import template

register = template.Library()

@register.filter
def has_group(user, group_name):
    """Devuelve True si el user está en el grupo llamado group_name."""
    return user.groups.filter(name=group_name).exists()
