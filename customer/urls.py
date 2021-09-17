from django.urls import path
from customer.views import (update_profile, set_address, ShowCustomerAddress, edit_address, delete_address)

app_name = 'customer'
urlpatterns = [
    path('update_profile/<int:pk>',update_profile,name='update_profile'),
    path('set-address/',set_address,name='set_address'),
    path('show-address/',ShowCustomerAddress.as_view(),name='show_address'),
    path('edit-address/<int:pk>',edit_address,name='edit_address'),
    path('delete_address/<int:pk>',delete_address,name='delete_address'),
]