from django.db import models
from management.models import CustomUser



class Customer(CustomUser):
    is_staff = False
    is_superuser = False

    class Meta:
        verbose_name = 'Customer'



class Address(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    location = models.TextField()

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
