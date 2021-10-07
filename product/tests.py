from django.conf import settings
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from product.models import Product, Category


class ProductViewTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Digital')
        for i in range(5):
            Product.objects.create(name=f'mobile{i}', category=self.category, real_price=i ** 2, inventory=10,
                                   content='something', image=f'{settings.BASE_DIR}/media/shop.png')

    def test_show_products(self):
        response = self.client.get(reverse('product:show_products'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('product:show_products', kwargs={'id': self.category.id}))
        self.assertEqual(response.status_code, 200)

    def test_ProductDetail(self):
        product = Product.objects.first()
        response = self.client.get(reverse('product:detail_product', kwargs={'pk': product.id}))
        self.assertEqual(response.status_code, 200)
