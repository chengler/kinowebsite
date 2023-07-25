from django import template
register = template.Library()

@register.filter(name='zehntel')
def zehntel(value):
    try:
        return int(value) / int(10)
    except (ValueError, ZeroDivisionError):
        return 0
    