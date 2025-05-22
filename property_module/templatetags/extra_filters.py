from django import template

register = template.Library()

@register.filter
def floatformat_custom(value, precision=0):
    try:
        return f'{float(value):.{precision}f}'
    except (ValueError, TypeError):
        return value

@register.filter
def to_range(value):
    return range(1, value)