from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from customer.api.serializers import CusotmerSerializer, LoginSerializer, ChangePasswordSerializer, \
    PasswordResetSerializer, PasswordResetConfirmSerializer
from customer.models import Customer



class EditCustomerProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CusotmerSerializer
    queryset = Customer.objects.all()






class CustomerCreate(generics.CreateAPIView):
    model = Customer
    serializer_class = CusotmerSerializer

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/register-customer.html'


    def get(self, request):
        serializer = self.get_serializer()
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = CusotmerSerializer(data=request.data)
        if not serializer.is_valid():
            # return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
            return Response({'serializer': serializer, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return redirect('core:index')

    def perform_create(self, serializer):

        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class CustomerLogin(generics.CreateAPIView):
    model = Customer
    serializer_class = LoginSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/login.html'



    def get(self, request,*args,**kwargs):
        serializer = self.get_serializer()
        return Response({'serializer': serializer})

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            login(request, serializer.validated_data['user'])
            if request.data['next']:
                return HttpResponseRedirect(redirect_to=request.data['next'])
            return redirect('core:index')
        else:
            return Response({'serializer':serializer,'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def get(self, request):
        if isinstance(self.request.user,AnonymousUser):
            return Response({'error':'just logged in user can log out'},status=status.HTTP_400_BAD_REQUEST)

        logout(request)
        return redirect('core:index')

class ChangePasswordView(generics.RetrieveUpdateDestroyAPIView):
    model = Customer
    serializer_class = ChangePasswordSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/change_password.html'
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.get_serializer()
        return Response({'serializer': serializer})

    def post(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.validated_data['old_password']):
                return Response({'serializer':serializer,'errors':{'error':[_(f'Invalid old password for user : {self.request.user.username}')]}},status=status.HTTP_406_NOT_ACCEPTABLE)

            self.object.set_password(serializer.validated_data['new_password'])
            self.object.save()
            user = authenticate(username=self.object.username,password=self.object.password)
            messages.info(request, _('Password changed successfully'))
            login(request,user=user)
            return redirect('core:index')

        return Response({'serializer':serializer,'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)




class PasswordResetView(GenericAPIView):

    """
    Calls Django Auth PasswordResetForm save method.
    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)


        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"success": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(GenericAPIView):

    """
    Password reset e-mail link is confirmed, therefore this resets the user's password.
    Accepts the following POST parameters: new_password1, new_password2
    Accepts the following Django URL arguments: token, uid
    Returns the success/fail message.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")})

