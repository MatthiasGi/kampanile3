from django import template

from ..models.conditions import CONDITION_LOOKUP

register = template.Library()


@register.filter
def type_to_name(val) -> str:
    if val in CONDITION_LOOKUP:
        return CONDITION_LOOKUP[val].meta.label
    return "Unknown"


@register.filter
def type_to_icon(val) -> str:
    if val in CONDITION_LOOKUP:
        return CONDITION_LOOKUP[val].meta.icon
    return ""
