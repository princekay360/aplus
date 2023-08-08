from django import template
from ..models import *

register = template.Library()


@register.inclusion_tag('aplus_app/student/base.html', takes_context=True)
def app_navs(context, active):
    return {
        "me": context['me'],
        "me_name_0": context['me_name_0'],
        "active": active,
    }

