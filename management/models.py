from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, AbstractUser, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import set_staff_group

# Create your models here.


class DiscountCode(models.Model):
    code = models.CharField(_('code'),max_length=50, unique=True)
    valid_from = models.DateTimeField(_('valid from'))
    valid_to = models.DateTimeField(_('valid to'))
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(_('status'))

    def __str__(self):
        return self.code

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, phone, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):
    phone = models.CharField(_('Phone number'), max_length=20,unique=True)
    image = models.FileField(_('image'),upload_to='user_images',null=True,blank=True)
    password_again = models.CharField(_('password again'),max_length=128)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone','email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Manager(CustomUser):

    class Meta:
        verbose_name = 'Manager'
    def save(self, *args, **kwargs):
        self.is_superuser = True
        self.is_staff = True
        self.is_active = True
        super(Manager,self).save(*args,**kwargs)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'




class Staff(CustomUser):

    class Meta:
        verbose_name = 'Staff'

    def save(self, *args, **kwargs):
        self.is_superuser = False
        self.is_staff = True
        self.is_active = True
        group = set_staff_group()
        super(Staff,self).save(*args,**kwargs)
        group.save()
        group.user_set.add(self)







