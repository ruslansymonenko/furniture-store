from django import template

from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def set_url_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)

    return urlencode(query)