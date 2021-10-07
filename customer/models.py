from django.db import models
from management.models import CustomUser
from django.utils.translation import gettext_lazy as _



class Customer(CustomUser):
    def save(self, *args, **kwargs):
        self.is_superuser = False
        self.is_staff = False
        self.is_active = True
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Customer')




class Address(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    country = models.CharField(_('country'),max_length=100)
    city = models.CharField(_('city'),max_length=100)
    location = models.TextField(_('location'))

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return f'{self.country} - {self.city} - {self.location}'


