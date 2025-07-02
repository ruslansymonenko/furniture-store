from django.http import JsonResponse
from django.views import View

from app.messages import SUCCESS_MESSAGES
from cart.mixins import CartMixin
from cart.models import Cart
from goods.models import Product


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)

        cart = self.get_cart(request, product=product)

        if cart:
            cart.quantity += 1
            cart.save()
        else:
            user = request.user if request.user.is_authenticated else None
            session_key = None if request.user.is_authenticated else request.session.session_key

            Cart.objects.create(
                user=user,
                session_key=session_key,
                product=product,
                quantity=1
            )

        response_data = {
            'message': SUCCESS_MESSAGES['cart_added'],
            "cart_item_html": self.render_cart(request),
        }

        return  JsonResponse(response_data)


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity

        cart.delete()

        response_data = {
            'message': SUCCESS_MESSAGES['cart_removed'],
            "cart_item_html": self.render_cart(request),
            "quantity_deleted": quantity,
        }

        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        cart = self.get_cart(request, cart_id=cart_id)
        cart.quantity = request.POST.get('quantity')

        cart.save()

        quantity = cart.quantity

        response_data = {
            'message': SUCCESS_MESSAGES['cart_updated'],
            "cart_item_html": self.render_cart(request),
            "quantity": quantity,
        }

        return JsonResponse(response_data)