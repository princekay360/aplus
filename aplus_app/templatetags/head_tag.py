from django import template
from ..models import *

register = template.Library()


@register.inclusion_tag('aplus_app/head_tag.html')
def html_head_tag(title):
    return {
        "title": title
    }
