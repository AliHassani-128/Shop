from django.conf import settings
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from customer.models import Customer, Address
from order.models import Order
from product.models import Product, Category


class OrderViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='digital')
        self.product = Product.objects.create(category=self.category, name='mobile',
                                              image=f'{settings.BASE_DIR}/media/shop.png', content='something ...',
                                              inventory=10, real_price=100)
        self.customer = Customer.objects.create(username='Ali12', first_name='Ali'
                                                , last_name='Hassani', email='example@example.com'
                                                , phone='09123456789')

        self.customer.set_password('admin')
        self.customer.save()

    def test_AddCartHomePage(self):
        # add to anonymous user cart
        response = self.client.get(reverse('order:add_to_cart_home_page'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)

        # add to login user cart and fetch with before login cart
        self.client.login(username=self.customer.username, password='admin')
        response = self.client.get(reverse('order:add_to_cart_home_page'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.filter(customer=self.customer).count(), 1)
        order = Order.objects.get(customer=self.customer)
        self.assertEqual(order.quantity, 2)

        response = self.client.get(reverse('order:add_to_cart_home_page'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(customer=self.customer)
        self.assertEqual(order.quantity, 3)

    def test_add_to_cart(self):
        response = self.client.get(reverse('order:add_to_cart_home_page'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('order:add_to_cart'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        order = Order.objects.last()
        self.assertEqual(order.quantity, 2)

        self.product.inventory = 0
        self.product.save()
        response = self.client.get(reverse('order:add_to_cart'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 400)

        self.product.inventory = 10
        self.product.save()

    def test_delete_from_cart(self):
        response = self.client.get(reverse('order:add_to_cart_home_page'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        order = Order.objects.last()
        self.assertEqual(order.quantity, 1)

        response = self.client.get(reverse('order:delete_from_cart'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.all().count(), 0)

        response = self.client.get(reverse('order:delete_from_cart'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 400)

    def test_order_list(self):
        response = self.client.get(reverse('order:add_to_cart_home_page'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('order:order_list'))
        self.assertEqual(response.status_code, 200)

        self.client.login(username=self.customer.username, password='admin')
        response = self.client.get(reverse('order:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.all().count(), 1)

        response = self.client.get(reverse('order:add_to_cart'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(customer=self.customer)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(Order.objects.filter(customer=self.customer).count(), 1)

    def test_final_order(self):
        # request to final order view without login and redirect to login page
        response = self.client.get(reverse('order:final_order'))
        self.assertEqual(response.status_code, 302)

        # request to final order with out any order for customer and redirect to index
        self.client.login(username=self.customer.username, password='admin')
        response = self.client.get(reverse('order:final_order'))
        self.assertEqual(response.status_code, 302)

        # request to final order with out address for customer and redirect to address view
        response = self.client.get(reverse('order:add_to_cart_home_page'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('order:final_order'))
        self.assertEqual(response.status_code, 302)

        Address.objects.create(customer=self.customer, country="IRAN", city="Tehran", location="some where ...")
        response = self.client.get(reverse('order:add_to_cart_home_page'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('order:final_order'))
        self.assertEqual(response.status_code, 200)

    def test_final_pay(self):
        # request to final pay view without login and redirect to login page
        response = self.client.get(reverse('order:final_pay', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # request to final pay view after login and without have any order history redirect to index
        self.client.login(username=self.customer.username, password='admin')
        response = self.client.get(reverse('order:final_pay', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # request to final pay view without send address id by post and redirect to final order page to select address
        address = Address.objects.create(customer=self.customer, country="IRAN", city="Tehran",
                                         location="some where ...")
        response = self.client.get(reverse('order:add_to_cart_home_page'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('order:final_order'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('order:final_pay', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 302)

        # request to final pay with all things that view need and after the process redirect to index(should redirect to payment gateway)
        response = self.client.post(reverse('order:final_pay', kwargs={'id': 1}), data={'address': address.id})
        self.assertEqual(response.status_code, 302)

    def test_delete_order(self):
        self.client.login(username=self.customer.username, password='admin')
        Address.objects.create(customer=self.customer, country="IRAN", city="Tehran", location="some where ...")
        response = self.client.get(reverse('order:add_to_cart_home_page'), data={'product': self.product.id})
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('order:final_order'))
        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(customer=self.customer)

        response = self.client.get(reverse('order:delete_order', kwargs={'id': order.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.all().count(), 0)
