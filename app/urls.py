from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

from app.settings import DEBUG, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('goods/', include('goods.urls', namespace='goods')),
    path('user/', include('user.urls', namespace='user')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
]

if DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)