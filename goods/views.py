from django.http import Http404
from django.views.generic import DetailView, ListView

from app.constants import PAGES_NAMES
from goods.models import Product
from goods.utils import q_search


class CatalogView(ListView):
    model = Product
    template_name = 'goods/catalog.html'
    context_object_name = 'goods'
    paginate_by = 6
    allow_empty = False

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        on_sale = self.request.GET.get('on_sale', None)
        order_by = self.request.GET.get('order_by', None)
        query = self.request.GET.get('q', None)

        if category_slug == 'all-goods':
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)

            if not goods.exists():
                raise Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != 'default':
            goods = goods.order_by(order_by)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = PAGES_NAMES['catalog_page']
        context['slug_url'] = self.kwargs.get('category_slug')
        return context


class ProductView(DetailView):
    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_object(self):
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{PAGES_NAMES['product_page']} - {self.object.name}'
        return context
