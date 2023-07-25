from django import template
register = template.Library()

@register.filter
def space2plus(value):
    return value.replace(" ","+")