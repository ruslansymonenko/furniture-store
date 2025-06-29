from django.contrib import admin

from cart.admin import CartTabAdmin
from orders.admin import OrderTabularAdmin
from user.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']

    inlines = [CartTabAdmin, OrderTabularAdmin]
