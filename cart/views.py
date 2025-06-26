from django.contrib import messages
from django.shortcuts import redirect

from app.messages import SUCCESS_MESSAGES
from cart.models import Cart
from goods.models import Product


def cart_add(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, product=product)

        if cart.exists():
            cart = cart.first()

            if cart:
                cart.quantity += 1
                cart.save()
                messages.success(request, SUCCESS_MESSAGES['cart_added'])
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
            messages.success(request, SUCCESS_MESSAGES['cart_added'])

    return redirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, product_slug):
    ...

def cart_change(request, product_slug):
    ...