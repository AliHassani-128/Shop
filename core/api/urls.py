from django.urls import path, include

urlpatterns = [
    path('customer/',include('customer.api.urls')),
    path('order/',include('order.api.urls')),

]