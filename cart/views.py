from django.http import JsonResponse
from django.template.loader import render_to_string

from app.messages import SUCCESS_MESSAGES
from cart.models import Cart
from cart.utils import get_user_cart
from goods.models import Product


def cart_add(request):
    product_id = request.POST.get('product_id')
    product = Product.objects.get(id=product_id)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, product=product)

        if cart.exists():
            cart = cart.first()

            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)


    user_cart = get_user_cart(request)
    cart_item_html = render_to_string(
        "cart/includes/cart.html", {'cart': user_cart}, request=request
    )

    response_data = {
        'message': SUCCESS_MESSAGES['cart_added'],
        "cart_item_html": cart_item_html,
    }

    return  JsonResponse(response_data)


def cart_remove(request):
    cart_id = request.POST.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity

    cart.delete()

    user_cart = get_user_cart(request)
    cart_item_html = render_to_string(
        "cart/includes/cart.html", {'cart': user_cart}, request=request
    )

    response_data = {
        'message': SUCCESS_MESSAGES['cart_removed'],
        "cart_item_html": cart_item_html,
        "quantity_deleted": quantity,
    }

    return  JsonResponse(response_data)

def cart_change(request, product_slug):
    ...