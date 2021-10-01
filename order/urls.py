from django.urls import path

from order.views import add_to_cart_home_page, order_list, add_to_cart, delete_from_cart, final_order, final_pay, \
    delete_order, All_Orders_History

app_name = 'order'
urlpatterns = [
    path('add-to-cart-home-page/',add_to_cart_home_page,name='add_to_cart_home_page'),
    path('order-list/',order_list,name='order_list'),
    path('add-to-cart/',add_to_cart,name='add_to_cart'),
    path('delete-from-cart/',delete_from_cart,name='delete_from_cart'),
    path('final-order/',final_order,name='final_order'),
    path('final-pay/<int:id>',final_pay,name='final_pay'),
    path('delete-order/<int:id>',delete_order,name='delete_order'),
    path('all_last_orders/',All_Orders_History.as_view(),name='all_last_orders'),
]