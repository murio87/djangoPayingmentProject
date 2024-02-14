from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop_home, name='shop'),
    path('delete/<id>', views.delete, name='delete'),
    #path('update/<id>', views.update_view_product, name='update'),
    path('pay/<id>', views.pay, name='pay'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
