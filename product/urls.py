from django.conf.urls import url
from django.urls import path

from product.views import show_products, ProductDetail

app_name = 'product'
urlpatterns = [
    url(r'^all_products/$', show_products, name='show_products'),
    url(r'^all_products/(?P<id>\w+)/$', show_products, name='show_products'),
    path('detail-product/<int:pk>',ProductDetail.as_view(),name='detail_product')
]
