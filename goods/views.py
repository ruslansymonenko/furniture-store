from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from goods.models import Product


def catalog(request, category_slug, page=1):
    if category_slug == 'all-goods':
        goods = Product.objects.all()
    else:
        goods = Product.objects.filter(category__slug=category_slug)

    paginator = Paginator(goods, 6)
    current_page_goods = paginator.page(page)

    print(current_page_goods)

    context = {
        'title': 'Catalog',
        'goods': current_page_goods,
        'slug_url': category_slug
    }

    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    context = {
        'product': product,
    }

    return render(request, 'goods/product.html', context=context)
