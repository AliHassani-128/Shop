from django.urls import path

from customer.views import index

app_name = 'customer'
urlpatterns = [
    path('', index, name='index'),
]