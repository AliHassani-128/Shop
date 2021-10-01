from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from management.models import CustomUser

class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField()

    def __str__(self):
        return self.code



class Customer(CustomUser):
    def save(self, *args, **kwargs):
        self.is_superuser = False
        self.is_staff = False
        self.is_active = True
        super(Customer, self).save(*args, **kwargs)

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

    def __str__(self):
        return f'{self.country} - {self.city} - {self.location}'


