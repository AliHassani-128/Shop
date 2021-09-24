from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from product.api.serializers import ProductSerializer
from product.models import Product


class ProductsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination