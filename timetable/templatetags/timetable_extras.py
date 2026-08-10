from django import template

register = template.Library()


@register.filter
def dict_get(d, key):
    """Get value from a dict by key in templates."""
    if isinstance(d, dict):
        return d.get(key, [])
    return []
