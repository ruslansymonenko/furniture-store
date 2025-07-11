from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart_add/', views.CartAddView.as_view(), name='cart_add'),
    path('cart_remove/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart_change/', views.CartChangeView.as_view(), name='cart_change'),
]