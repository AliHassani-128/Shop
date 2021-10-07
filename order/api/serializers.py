from rest_framework import serializers

from management.models import DiscountCode


class DiscountCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=128,  style={'placeholder': 'Discount Code'})

    def validate(self, attrs):
        if attrs['code']:
            try:
                discount_code = DiscountCode.objects.get(code=attrs['code'])
            except DiscountCode.DoesNotExist:
                raise serializers.ValidationError('The discount code does not exists!')
            return {'code': discount_code.code}

