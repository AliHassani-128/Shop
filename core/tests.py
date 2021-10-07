from django.conf import settings
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from product.models import Product, Category


class CoreViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Digital')
        for i in range(5):
            Product.objects.create(name=f'mobile{i}', category=self.category, real_price=i ** 2, inventory=10,
                                   content='something', image=f'{settings.BASE_DIR}/media/shop.png')


    def test_index(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code,200)


    def test_search(self):
        # search with product name
        product = Product.objects.first()
        response = self.client.post(reverse('core:search'),data={'search':product.name})
        self.assertEqual(response.status_code,200)

        # search with category name
        response = self.client.post(reverse('core:search'), data={'search': product.category})
        self.assertEqual(response.status_code, 200)

        # product not found
        response = self.client.post(reverse('core:search'), data={'search': product.id})
        self.assertEqual(response.status_code, 302)
