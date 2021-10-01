from django.urls import path
from core.views import index, search

app_name = 'core'
urlpatterns = [
    path('', index, name='index'),
    path('search/',search,name='search'),
]