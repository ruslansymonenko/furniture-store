from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import redirect
from django.forms import ValidationError
from django.urls import reverse_lazy
from django.views.generic import FormView

from app.constants import PAGES_NAMES
from app.messages import SUCCESS_MESSAGES
from cart.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem

class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create-order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('user:profile')

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    order = Order.objects.create(
                        user=user,
                        phone=form.cleaned_data['phone'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get'],
                    )

                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.sell_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(
                                f'The required quantity of goods is not in stock, available quantity: {product.quantity}')

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )

                        product.quantity = product.quantity - quantity
                        product.save()

                    cart_items.delete()

                    messages.success(self.request, SUCCESS_MESSAGES['successful_order'])
                    return redirect('user:profile')

        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect('order:create_order')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['phone'] = self.request.user.phone

        return initial

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error: {error}")
        return redirect('order:create_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = PAGES_NAMES['order_page']
        return context