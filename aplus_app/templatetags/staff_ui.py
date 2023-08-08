from django import template
from ..models import *

register = template.Library()


@register.inclusion_tag('aplus_app/staff/base.html', takes_context=True)
def staff_app_navs(context, active):
    return {
        "staff": context['staff'],
        "staff_name_0": context['staff_name_0'],
        "active": active,
    }

