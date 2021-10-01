from django.urls import path

from order.api.views import DiscountCodeView

urlpatterns = [
    path('discount/',DiscountCodeView.as_view(),name='set_discount'),
    # path('discount/<int:id>',DiscountCodeView.as_view(),name='set_discount'),
]