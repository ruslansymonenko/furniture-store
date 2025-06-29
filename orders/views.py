from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.forms import ValidationError

from app.messages import SUCCESS_MESSAGES
from cart.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = request.user
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
                                raise ValidationError(f'The required quantity of goods is not in stock, available quantity: {product.quantity}')

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

                        messages.success(request, SUCCESS_MESSAGES['successful_order'])
                        return redirect('user:profile')

            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('order:create_order')


        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': request.user.phone,
        }

        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Create Order',
        'form': form,
    }

    return render(request, 'orders/create-order.html', context=context)