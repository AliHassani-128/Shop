from django.contrib import admin

# Register your models here.
from product.models import Product, Category

from django.contrib import admin
from django import forms

class ProductImageForm(forms.ModelForm):
   class Meta:
       model = Product
       fields = '__all__'

   def clean_image(self):
       img = self.cleaned_data.get('image')
       if not img:
           return img
       width = 800
       height = 400
       if any(dim > width for dim in img.image.size):
           # Resize too large image up to the max_size
           from PIL import Image
           i = Image.open(img.file)
           fmt = i.format.lower()
           i.thumbnail((width, height))
           # We must reset io.BytesIO object, otherwise resized image bytes
           # will get appended to the original image
           img.file = type(img.file)()
           i.save(img.file, fmt)
       return img

class ProductAdmin(admin.ModelAdmin):
    form = ProductImageForm

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)

