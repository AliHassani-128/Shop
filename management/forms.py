from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser
from django import forms

class UserAdminCreationForm(forms.ModelForm):
    phone = forms.CharField(label='phone', max_length=20, required=True)
    image = forms.ImageField(label="image", required=False)
    password = forms.CharField(max_length=120,widget=forms.PasswordInput())
    password_again= forms.CharField(max_length=120,widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'image', 'phone',
                  'email', 'password', 'password_again','is_superuser','is_staff','is_active',
                  'user_permissions')

    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")
        if password is not None and password != password_again:
            self.add_error("password_again", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(UserAdminCreationForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        exclude = ('password_again',)


