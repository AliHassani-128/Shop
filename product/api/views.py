from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from product.api.serializers import ProductSerializer
from product.models import Product


class ProductsPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data,
            'page_number': self.get_page_number(self.request, self.page.paginator),
        })


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination
