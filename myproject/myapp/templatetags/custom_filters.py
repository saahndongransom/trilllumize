# custom_filters.py

from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return float(value) * int(arg)
    except (ValueError, TypeError):
        return value
