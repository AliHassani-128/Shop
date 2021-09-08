from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Manager(User):
    phone = models.IntegerField('Phone number', unique=True)
    image = models.FileField(upload_to='manager_image', blank=True, null=True)
    password_again = models.CharField(max_length=128)
    is_staff = True
    is_superuser = True

    class Meta:
        verbose_name = 'Manager'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Staff(User):
    phone = models.IntegerField('Phone number', unique=True)
    image = models.FileField(upload_to='staff_image', blank=True, null=True)
    password_again = models.CharField(max_length=128)
    is_staff = True
    is_superuser = False

    class Meta:
        verbose_name = 'Staff'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
