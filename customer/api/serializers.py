from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core import validators
from django.utils.encoding import force_text
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode as uid_decoder
from customer.models import Customer
from django.utils.translation import gettext_lazy as _


class CusotmerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True,  style={ 'placeholder': 'Username'})
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password', 'placeholder': 'Password'})
    password_again = serializers.CharField(write_only=True, required=True,style={'input_type': 'password', 'placeholder': 'Password Again'})
    email = serializers.CharField(write_only=True,required=True,style={'placeholder': 'Email'})
    class Meta:
        model = Customer
        depth = 1
        fields = [_('username'),_('first_name'),_('last_name'),_('password'),_('password_again'),_('email'),_('phone'),_('image')]


    def create(self, validated_data):
        customer = Customer.objects.create(username=validated_data['username'],
                                           first_name=validated_data['first_name'],
                                           last_name=validated_data['last_name'],
                                           password=make_password(validated_data['password']),
                                           email=validated_data['email'],
                                           phone=validated_data['phone'],
                                           image=validated_data['image']
                                           )
        return customer
    def validate(self, attrs):
        if attrs['password'] != attrs['password_again']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if not attrs['email']:
            raise serializers.ValidationError({'emil':'Email field is required'})
        if not attrs['phone']:
            raise serializers.ValidationError({'phone':'Phone field is required'})
        return attrs

    def validate_username(self, username):
        if len(username) < 4 or len(username) > 15:
            raise ValidationError('Username must be between 4 and 15 characters long')
        return username




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128,  style={'placeholder': 'Username'})

    password = serializers.CharField(write_only=True,
                                         style={'input_type': 'password', 'placeholder': 'Password'})

    def validate(self, attrs):
        if attrs['username'] and attrs['password']:
            try:
                Customer.objects.get(username=attrs['username'])
            except Customer.DoesNotExist:
                raise serializers.ValidationError('Customer with this username does not exists please sign up first!')
            user = authenticate(username=attrs['username'], password=attrs['password'])
        else:
            raise serializers.ValidationError('Username and password are required')
        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}

class ChangePasswordSerializer(serializers.Serializer):
    model = Customer
    old_password = serializers.CharField(write_only=True, required=True,
                                         style={'placeholder': 'Old Password'})
    new_password = serializers.CharField(write_only=True, required=True,
                                         style={'input_type': 'password', 'placeholder': 'New Password'},validators=[validators.MinLengthValidator(6),validators.RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumericcharacters are allowed.')])




class PasswordResetSerializer(serializers.Serializer):

    """
    Serializer for requesting a password reset e-mail.
    """

    email = serializers.EmailField()

    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        if not Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))

        return value

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    set_password_form_class = SetPasswordForm

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        # Decode the uidb64 to uid to get User object
        try:
            uid = force_text(uid_decoder(attrs['uid']))
            self.user = Customer._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self):
        self.set_password_form.save()
