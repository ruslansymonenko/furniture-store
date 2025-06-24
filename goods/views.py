from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from goods.models import Product
from goods.utils import q_search


def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all-goods':
        goods = Product.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Product.objects.filter(category__slug=category_slug)

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

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
