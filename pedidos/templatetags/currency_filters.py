from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def currency_cop(value):
    """
    Formatea un valor numérico como pesos colombianos
    Ejemplo: 250000 -> $250.000
    """
    try:
        # Convertir a entero para eliminar decimales
        value = int(float(value))
        # Usar intcomma para agregar separadores de miles
        formatted = intcomma(value)
        return f"${formatted}"
    except (ValueError, TypeError):
        return f"${value}"

@register.filter
def currency_cop_detailed(value):
    """
    Formatea un valor numérico como pesos colombianos con más detalle
    Ejemplo: 250000 -> $250.000 COP
    """
    try:
        value = int(float(value))
        formatted = intcomma(value)
        return f"${formatted} COP"
    except (ValueError, TypeError):
        return f"${value} COP"