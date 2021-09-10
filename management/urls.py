from django.urls import path, include
from .views import register_manager

app_name = 'management'
urlpatterns = [

    path('register-manager/',register_manager,name='register-manager'),
]