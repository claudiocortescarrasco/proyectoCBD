import re
from django import template

register = template.Library()

@register.filter
def regex_findall(value, pattern):
    """
    Aplica re.findall() sobre el valor con el patrón dado.
    """
    return re.findall(pattern, value)
