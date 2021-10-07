from django.urls import path

from product.api.views import ProductView

urlpatterns = [
    path('', ProductView.as_view(), name='products'),
]