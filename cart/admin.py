from django.contrib import admin

from cart.models import Cart

class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = 'product', 'quantity', 'created_at'
    search_fields = 'product', 'user__username', 'product__name'
    readonly_fields = ('created_at',)
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_link', 'product', 'quantity', 'created_at']
    list_filter = ['created_at', 'user__username', 'product__name']

    @admin.display(description='User')
    def user_link(self, obj):
        if obj.user:
            return str(obj.user.username)
        return 'Unknown User'

    @admin.display(description='User')
    def product_display(self, obj):
        return str(obj.product.name)


