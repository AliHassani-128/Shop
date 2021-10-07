from django.test import TestCase

from rest_framework.test import APITestCase
# Create your tests here.
from django.urls import reverse

from customer.models import Customer, Address


class CustomerViewTest(TestCase):
    def setUp(self):
        self.user = Customer.objects.create(username='Ali123', first_name='Ali'
                                            , last_name='Hassani', email='example@example.com'
                                            , phone='09123456789')
        self.user.set_password('admin')
        self.user.save()

    def test_update_profile(self):
        self.client.login(username=self.user.username, password='admin')
        response = self.client.get(reverse('customer:update_profile', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('customer:update_profile', kwargs={'pk': self.user.id}),
                                    data={'password': 'admin'})
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse('customer:update_profile', kwargs={'pk': self.user.id}),
                                    data={'username': 'ali', 'first_name': 'Ali', 'last_name': 'hasani',
                                          'email': 'mail@mail.com', 'phone': '09369852147', 'image': ''})
        self.assertEqual(response.status_code, 302)

    def test_set_address(self):
        self.client.login(username=self.user.username, password='admin')
        response = self.client.get(reverse('customer:set_address'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('customer:set_address'),
                                    data={'country': 'IRAN', 'city': 'Tehran', 'location': 'some where in iran'})
        self.assertEqual(response.status_code, 302)

    def test_ShowCustomerAddress(self):
        self.client.login(username=self.user.username, password='admin')
        response = self.client.get(reverse('customer:show_address'))
        self.assertEqual(response.status_code, 200)

    def test_edit_address(self):
        address = Address.objects.create(customer=self.user, country='IRAN', city='Tehran', location='Navab,Sina')
        self.client.login(username=self.user.username, password='admin')
        response = self.client.get(reverse('customer:edit_address', kwargs={'pk': address.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('customer:edit_address', kwargs={'pk': address.id}),
                                    data={'country': 'Germany', 'city': 'Berlin', 'location': 'some where in Berlin'})
        self.assertEqual(response.status_code, 302)

    def test_delete_address(self):
        address = Address.objects.create(customer=self.user, country='IRAN', city='Tehran', location='Navab,Sina')
        response = self.client.get(reverse('customer:edit_address', kwargs={'pk': address.id}))
        self.assertEqual(response.status_code, 302)


class TestCustomerAPI(APITestCase):

    def setUp(self):
        self.user = Customer.objects.create(username='Ali123', first_name='Ali'
                                            , last_name='Hassani', email='example@example.com'
                                            , phone='09123456789')
        self.user.set_password('admin')
        self.user.save()

    def test_CustomerCreate(self):
        response = self.client.get(reverse('register_customer'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('register_customer'),
                                    data={'username': 'alihassani', 'first_name': 'Ali', 'last_name': 'Hassani',
                                          'password': 'admin12345', 'password_again': 'admin12345',
                                          'email': 'ali@example.com', 'phone': '09123456189', 'image': ''})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.all().count(),2)
    def test_CustomerLogin(self):
        response = self.client.get(reverse('login_customer'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('login_customer'),
                                    data={'username': self.user.username, 'password': 'admin', 'next': ''})

        self.assertEqual(response.status_code, 302)

    def test_LogoutView(self):
        response = self.client.get(reverse('logout_customer'))
        self.assertEqual(response.status_code, 400)

        self.client.login(username=self.user.username, password='admin')
        response = self.client.get(reverse('logout_customer'))
        self.assertEqual(response.status_code, 302)

    def test_ChangePasswordView(self):
        # test with out login user
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 403)
        # test with login user
        self.client.login(username=self.user.username, password='admin')
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('change_password'),
                                    data={'old_password': 'admin111', 'new_password': 'admin123'})
        self.assertEqual(response.status_code, 406)

        response = self.client.post(reverse('change_password'),
                                    data={'old_password': 'admin', 'new_password': 'admin123'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('change_password'))
        self.assertEqual(response.status_code, 400)

    def test_PasswordResetView(self):
        response = self.client.post(reverse('password_reset'), data={'email': self.user.email})
        self.assertEqual(response.status_code, 200)

        # test invalid password that is not in the db
        response = self.client.post(reverse('password_reset'), data={'email': 'ali@gmail.com'})
        self.assertEqual(response.status_code, 400)

        # test post method with out sending any data
        response = self.client.post(reverse('password_reset'), data={})
        self.assertEqual(response.status_code, 400)
