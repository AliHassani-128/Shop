from django.urls import path, include
from django.conf.urls import url

from customer.api.views import CustomerCreate, CustomerLogin, LogoutView, ChangePasswordView, PasswordResetView, \
    PasswordResetConfirmView, EditCustomerProfile


urlpatterns = [
    path('register/', CustomerCreate.as_view(), name='register_customer'),
    path('login/', CustomerLogin.as_view(), name='login_customer'),
    path('logout/', LogoutView.as_view(), name='logout_customer'),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    path('password/reset/', PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path('edit-profile/<int:pk>',EditCustomerProfile.as_view(),name='edit_profile'),
]
