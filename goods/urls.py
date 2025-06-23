from django.urls import path
from . import views

app_name = 'goods'

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<slug:category_slug>/', views.catalog, name='catalog'),
    path('catalog/<slug:category_slug>/<int:page>', views.catalog, name='catalog'),
    path('product/<slug:product_slug>/', views.product, name='product'),
]