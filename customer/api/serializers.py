from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from customer.models import Customer


class CusotmerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password] ,style={'input_type': 'password', 'placeholder': 'Password'})
    password_again = serializers.CharField(write_only=True, required=True , validators=[validate_password] ,style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = Customer
        depth = 1
        fields = ['username','first_name','last_name','password','password_again','email','phone','image']


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
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, required=True, style={'placeholder': 'Username'})

    password = serializers.CharField(write_only=True, required=True,
                                         style={'input_type': 'password', 'placeholder': 'Password'})

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}


