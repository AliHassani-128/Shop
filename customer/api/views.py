from django.contrib.auth import login, logout
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from customer.api.serializers import CusotmerSerializer, LoginSerializer
from customer.models import Customer


class CustomerCreate(generics.CreateAPIView):
    model = Customer
    serializer_class = CusotmerSerializer

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/register-customer.html'

    def get(self,request):
        serializer = CusotmerSerializer()
        return Response({'serializer': serializer})

    def post(self,request):
        serializer = CusotmerSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'serializer': serializer})
        else:
            serializer.save()
            return redirect('customer:index')
    def perform_create(self, serializer):

        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()



class CustomerLogin(generics.CreateAPIView):
    model = Customer
    serializer_class = LoginSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/login.html'

    def get(self,request):
        serializer = LoginSerializer()
        return Response({'serializer': serializer})


    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            login(request,serializer.validated_data['user'])
            return redirect('customer:index')
        else:
            return Response({'serializer':serializer})



class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return redirect('customer:index')




