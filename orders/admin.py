from django.contrib import admin

from orders.models import Order, OrderItem

class OrderItemTabularAdmin(admin.TabularInline):
    model = OrderItem
    fields = ("product_name", "price", "quantity")
    readonly_fields = ("product_name",)
    extra = 0

    def product_name(self, obj):
        return obj.name
    product_name.short_description = "Product"

class OrderTabularAdmin(admin.TabularInline):
    model = Order
    fields = ("requires_delivery", "status", "payment_on_get", "is_paid", "created_at", "delivery_address")
    search_fields = ['is_paid', 'created_at']

    readonly_fields = ("created_at",)
    extra = 0

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product_name", "name", "price", "quantity"
    search_fields = (
        "order__id",
        "product__name",
        "name",
    )

    @admin.display(description="Product")
    def product_name(self, obj):
        return obj.name

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = "id", "user_display", "requires_delivery", "status", "payment_on_get", "delivery_address", "is_paid", "created_at"
    search_fields = (
        "id",
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_at",
    )

    list_editable = ("status", "payment_on_get", "is_paid")

    readonly_fields = ("created_at",)
    list_filter = ("status", "is_paid", "created_at")
    inlines = (OrderItemTabularAdmin,)

    @admin.display(description='User')
    def user_display(self, obj):
        if obj.user:
            return str(obj.user.username)
        return 'Unknown User'

