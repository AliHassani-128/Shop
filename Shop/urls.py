from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('customer/', include('customer.urls')),
    path('api/v1/', include('core.api.urls')),
    path('product/', include('product.urls')),
    path('api/v1/', include('product.api.urls')),
    path('order/', include('order.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

