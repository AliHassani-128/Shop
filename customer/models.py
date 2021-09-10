from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Customer(User):
    phone = models.IntegerField('Phone number', unique=True)
    image = models.FileField(upload_to='customer_image',blank=True,null=True)
    is_staff = False
    is_superuser = False
    class Meta:
        verbose_name = 'Customer'


    def __str__(self):
            return f'{self.first_name} {self.last_name}'

class Address(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    address = models.TextField()
