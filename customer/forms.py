from django import forms

from customer.models import Customer, Address


class CustomerAdminForm(forms.ModelForm):
    pass

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['username','first_name','last_name','email','phone','image']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['location']

class EditAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('customer',)

