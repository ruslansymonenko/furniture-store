from django.db import models

from goods.models import Product
from user.models import User

class CartQuerySet(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)

        return 0

class Cart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='User')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Quantity')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    session_key = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Cart'

    objects = CartQuerySet.as_manager()

    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)

    def __str__(self):
        if self.user:
            return f'Cart | User: {self.user.username} | Product: {self.product.name} | Quantity: {self.quantity}'
        else: return f'Cart | Unknown user | Product: {self.product.name} | Quantity: {self.quantity}'

