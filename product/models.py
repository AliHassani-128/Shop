from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _



class Category(models.Model):
    name = models.CharField(_('category'),max_length=200,unique=True)
    parent = models.ForeignKey('Category',null=True,blank=True,related_name='children',on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def save(self, *args,**kwargs):
        if self.parent and self.parent.name == self.name:
            raise ValidationError(_('Category can not have same parent and children'))
        return super(Category,self).save(*args,**kwargs)

    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(_('name of product'),max_length=200)
    image = models.ImageField(_('image'),upload_to='product_image')
    content = models.TextField(_('description'))
    real_price = models.PositiveIntegerField(_('main price'))
    discount = models.PositiveIntegerField(_('discount'),null=True,blank=True,validators=[MinValueValidator(0), MaxValueValidator(100)])
    inventory = models.PositiveIntegerField(_('inventory'))

    def __str__(self):
        return f'{self.name} -- price:{self.real_price} -- Inventory:{self.inventory}'

    @property
    def discount_price(self):
        if self.discount:
            return self.real_price - (self.real_price * self.discount / 100)
        return self.real_price

    class Meta:
        ordering = ['-id']
