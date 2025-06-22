from django.shortcuts import render

from goods.models import Product


def catalog(request):
    products = Product.objects.all()

    context = {
        'title': 'Catalog',
        'goods': products
    }

    return render(request, 'goods/catalog.html', context)

def product(request):
    return render(request, 'goods/product.html')