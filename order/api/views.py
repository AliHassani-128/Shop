from django.http import JsonResponse
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from customer.models import Customer
from order.api.serializers import DiscountCodeSerializer
from order.models import OrderHistory
from management.models import DiscountCode


class DiscountCodeView(APIView):
    model = DiscountCode
    serializer_class = DiscountCodeSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order/set_discount.html'

    def get(self, request):
        serializer = DiscountCodeSerializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = DiscountCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({'error': 'The discount code does not exist!'})
        else:
            order = OrderHistory.objects.get(id=request.session.get('order_history'))
            customer = Customer.objects.get(id=request.user.id)
            if customer.discount_code:
                if customer.discount_code.code == serializer.validated_data['code']:
                    order.total_price -= (order.total_price * customer.discount_code.discount) / 100
                    customer.discount_code = None
                    order.save()
                    customer.save()

                    return JsonResponse({'total_price': order.total_price})
                else:
                    return JsonResponse({'error': 'Invalid discount code'})
            else:
                return JsonResponse({'error': 'You have not any discount code'})
