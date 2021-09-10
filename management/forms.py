from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Manager
from django import forms

class ManagerForm(UserCreationForm):
    phone = forms.CharField(label='phone', max_length=20, required=False)
    image = forms.ImageField(label="image", required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'image', 'phone',
                  'email', 'password1', 'password2',)

