# productos/templatetags/group_filters.py
from django import template

register = template.Library()

@register.filter
def has_group(user, group_name):
    """Devuelve True si el usuario pertenece al grupo group_name."""
    return user.groups.filter(name=group_name).exists()

@register.filter
def get_item(dictionary, key):
    """Permite acceder a un valor de diccionario usando una variable como clave."""
    return dictionary.get(key)
