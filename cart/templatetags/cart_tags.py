from django import template

from cart.models import Cart

register = template.Library()

@register.simple_tag()
def user_cart(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)

