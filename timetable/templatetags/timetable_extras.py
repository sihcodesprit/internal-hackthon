import datetime

from django import template

register = template.Library()


@register.filter
def dict_get(d, key):
    """Get value from a dict by key in templates."""
    if isinstance(d, dict):
        return d.get(key, [])
    return []


@register.filter
def duration_hours(start, end):
    """Hours between two time objects, for templates."""
    try:
        base = datetime.date.today()
        delta = datetime.datetime.combine(base, end) - datetime.datetime.combine(base, start)
        return round(delta.total_seconds() / 3600, 1)
    except (TypeError, ValueError, AttributeError):
        return 0
