from django.contrib import admin

# Register your models here.
from customer.forms import CusotmerRegisterForm, CustomerChangeForm
from customer.models import Customer, Address


admin.site.register(Address)



class CustomerAdmin(admin.ModelAdmin):
    form = CustomerChangeForm
    add_form = CusotmerRegisterForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    ordering = ('username',)
    readonly_fields = ('username','email','phone')

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}

        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


admin.site.register(Customer, CustomerAdmin)
