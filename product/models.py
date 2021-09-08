from django.db import models

# Create your models here.
from management.models import Staff


class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    parent = models.ForeignKey('Category',null=True,blank=True,on_delete=models.CASCADE)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_image')
    description = models.TextField()
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']








