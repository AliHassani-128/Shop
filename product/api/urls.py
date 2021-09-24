from django.urls import path

from product.api.views import ProductView

urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
]