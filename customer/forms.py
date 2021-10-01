from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from customer.models import Customer, Address


class CustomerAdminForm(forms.ModelForm):
    pass


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'image']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['location']


class EditAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('customer',)


class CusotmerRegisterForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone']

    def __init__(self, *args, **kwargs):
        super(CusotmerRegisterForm, self).__init__(*args, **kwargs)
        # del self.fields['password2']
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

class CustomerChangeForm(UserChangeForm):

    class Meta:
        fields = ['username','first_name','last_name','email','phone','discount_code','image']
