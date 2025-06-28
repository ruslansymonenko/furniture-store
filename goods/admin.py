from django.contrib import admin

from goods.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'category', 'price', 'discount', 'sell_price_display', 'quantity']
    list_editable = ['discount', 'quantity']
    search_fields = ['name', 'description', 'category__name']
    list_filter = ['discount', 'price', 'quantity']

    @admin.display(description='Sell Price')
    def sell_price_display(self, obj):
        return obj.sell_price()