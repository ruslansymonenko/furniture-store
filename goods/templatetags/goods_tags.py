from urllib.parse import urlencode
from django import template

from goods.models import Category

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.simple_tag(takes_context=True)
def set_url_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)

    return urlencode(query)