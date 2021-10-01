from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id','category','name','image','content','real_price','discount','inventory','discount_price']
        depth = 1