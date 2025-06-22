from django.shortcuts import render, get_object_or_404

from goods.models import Product


def catalog(request, category_slug):
    if category_slug == 'all-goods':
        goods = Product.objects.all()
    else:
        goods = Product.objects.filter(category__slug=category_slug)

    context = {
        'title': 'Catalog',
        'goods': goods
    }

    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    context = {
        'product': product,
    }

    return render(request, 'goods/product.html', context=context)
