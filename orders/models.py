from django.db import models

from goods.models import Product
from user.models import User

class OrderItemQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.product.price for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)

        return 0


class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, verbose_name="User", default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    requires_delivery = models.BooleanField(default=False, verbose_name="Requires delivery")
    delivery_address = models.CharField(max_length=11, verbose_name="Delivery address")
    payment_on_get = models.BooleanField(default=False, verbose_name="Payment on get")
    is_paid = models.BooleanField(default=False, verbose_name="Is paid")
    status = models.CharField(max_length=50, default='Pending', verbose_name="Status")

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order № {self.id} | {self.user.first_name} {self.user.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name="Order")
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, verbose_name="Product", null=True, blank=True, default=None)
    name = models.CharField(max_length=150, verbose_name="Name")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Price")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    objects = OrderItemQueryset.as_manager()

    def product_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        return f'Order Item | {self.name} | Order № {self.order.pk}'
