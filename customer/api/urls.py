from django.urls import path

from customer.api.views import CustomerCreate, CustomerLogin, LogoutView

urlpatterns = [
    path('register/',CustomerCreate.as_view(),name='register_customer'),
    path('login/',CustomerLogin.as_view(),name='login_customer'),
    path('logout/',LogoutView.as_view(),name='logout_customer'),
]