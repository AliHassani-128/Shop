from django.urls import path, include

urlpatterns = [
    path('customer/',include('customer.api.urls')),

]