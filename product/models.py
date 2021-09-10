from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    parent = models.ForeignKey('Category',null=True,blank=True,on_delete=models.CASCADE)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='product_image')
    content = models.TextField()
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()