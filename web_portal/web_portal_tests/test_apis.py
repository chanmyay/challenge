import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework_jwt.compat import get_user_model
from rest_framework_jwt.test import APIClient

from ..models import Order, Product, Customer, Branch, Organization
from ..serializers import OrderListSerializers


User = get_user_model()


class GetAllOrderTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        presetup_data = 5
        for data in range(presetup_data):
            organization = Organization.objects.create(
                name="Organization %s" % (data))
            branch = Branch.objects.create(
                name="Branch %s" % (data), organization=organization)
            customer = Customer.objects.create(
                name="Customer %s" % (data),
                email="user%s@mail.com" % (data), branch=branch)
            product = Product.objects.create(name="Product %s" % (data))
            for new_order in range(5):
                Order.objects.create(product=product,
                                     customer=customer,
                                     comments="comment %s" % new_order)

        self.email = 'testuser@email.com'
        self.username = 'testuser'
        self.password = 'testuserpassword'
        self.user = User.objects.create_user(
            self.username, self.email, self.password)

        self.data = {
            'username': self.username,
            'password': self.password
        }

    def test_get_all_orders_with_url(self):

        client = APIClient(enforce_csrf_checks=True)

        response = client.post('/token_get/', self.data, format='json')
        token = response.data['token']

        response = self.client.get(
            '/api/order_list', {},
            HTTP_AUTHORIZATION='CHALLENGE {}'.format(token))

        orders = Order.objects.all()
        serializer = OrderListSerializers(orders, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_orders_with_name(self):

        client = APIClient(enforce_csrf_checks=True)

        response = client.post('/token_get/', self.data, format='json')
        token = response.data['token']

        response = self.client.get(
            reverse('api_order_list'), {},
            HTTP_AUTHORIZATION='CHALLENGE {}'.format(token))

        orders = Order.objects.all()
        serializer = OrderListSerializers(orders, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_orders_without_token(self):

        response = self.client.get(
            reverse('api_order_list'), {},
            HTTP_AUTHORIZATION='CHALLENGE {}'.format(""))

        orders = Order.objects.all()
        serializer = OrderListSerializers(orders, many=True)
        self.assertNotEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_an_order(self):

        client = APIClient(enforce_csrf_checks=True)

        response = client.post('/token_get/', self.data, format='json')
        token = response.data['token']

        customer = Customer.objects.all()[0]
        product = Product.objects.all()[0]

        context = {
            'customer': customer.id,
            'product': product.id,
            'comments': 'testing'}

        response = self.client.post(reverse(
            'api_order_create'), context,
            HTTP_AUTHORIZATION='CHALLENGE {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_fail(self):

        client = APIClient(enforce_csrf_checks=True)

        response = client.post('/token_get/', self.data, format='json')
        token = response.data['token']

        customer = Customer.objects.all()[0]
        product = Product.objects.all()[0]

        context = {
            'customer': "",
            'product': "",
            'comments': 'testing'}

        response = self.client.post(reverse(
            'api_order_create'), context,
            HTTP_AUTHORIZATION='CHALLENGE {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
