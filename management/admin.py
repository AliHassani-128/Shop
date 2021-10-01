from django.contrib import admin

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import Manager, Staff, DiscountCode

admin.site.register(DiscountCode)



class CustomUserAdmin(admin.ModelAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    ordering = ('username',)

    def get_form(self, request, obj=None, **kwargs):

        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)




admin.site.register(Manager,CustomUserAdmin)
admin.site.register(Staff,CustomUserAdmin)

