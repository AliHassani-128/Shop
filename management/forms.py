from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser
from django import forms


class UserAdminCreationForm(forms.ModelForm):
    phone = forms.CharField(label='phone', max_length=20, required=True)
    image = forms.ImageField(label="image", required=False)
    password = forms.CharField(max_length=120, widget=forms.PasswordInput())
    password_again = forms.CharField(max_length=120, widget=forms.PasswordInput())
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'image', 'phone',
                  'email', 'password', 'password_again' ,'is_superuser', 'is_staff', 'is_active',
                  'user_permissions')



    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(UserAdminCreationForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a href=\"../password/\">this form</a>."))
    password_again = ReadOnlyPasswordHashField(label=("Password again"),)
    class Meta:
        model = CustomUser
        fields = '__all__'
