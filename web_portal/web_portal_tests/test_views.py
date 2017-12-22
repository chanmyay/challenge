from django.test import TestCase
from django.urls import reverse

from ..models import Order, Product, Customer, Branch, Organization

class OrderListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Create 21 order for pagination tests
        number_of_orders = 21
        organization = Organization.objects.create(name="Organization 1")
        branch = Branch.objects.create(name="Branch 1", organization=organization)
        customer = Customer.objects.create(name="test", email="test@mail.com",branch=branch)
        product = Product.objects.create(name="Product A")
        for order_number in range(number_of_orders):
            Order.objects.create(product=product, 
                    customer=customer, 
                    comments="comment %s"% order_number)
           
    def test_list_view_url_exists_at_desired_location(self): 
        response = self.client.get('/order/') 
        self.assertEqual(response.status_code, 200)  
           
    def test_list_view_url_accessible_by_name(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        
    def test_list_view_uses_correct_template(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order_list.html')
        
    def test_list_pagination_is_six(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue( len(response.context['order_list']) == 10)

    def test_lists_all_orders(self):
        # Get third page and confirm it has (exactly) remaining 1 items
        response = self.client.get(reverse('order_list')+'?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue( len(response.context['order_list']) == 1)

    def test_lists_page_not_exist(self):
        # Try to check fifth page that does not exist 
        response = self.client.get(reverse('order_list')+'?page=5')
        self.assertEqual(response.status_code, 404)


    def test_update_view_url_exists_at_desired_location(self): 
        order = Order.objects.all()[0]
        response = self.client.get('/order/%s/edit' % (order.id)) 
        self.assertEqual(response.status_code, 200)  
           
    def test_update_view_url_accessible_by_name(self):
        order = Order.objects.all()[0]
        response = self.client.get(reverse('order_update', kwargs={'pk':order.id}))
        self.assertEqual(response.status_code, 200)
        
    def test_update_view_uses_correct_template(self):
        order = Order.objects.all()[0]
        response = self.client.get(reverse('order_update', kwargs={'pk':order.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order_edit.html')


    def test_update_view_not_exist(self):
        response = self.client.post(reverse('order_update', kwargs={'pk':10000000000}))

        # try to delete the record that does not exist
        # will show page not fould
        self.assertEqual(response.status_code, 404)

    def test_update_view_update_existing_data_success(self):
        order = Order.objects.all()[0]
        response = self.client.get(reverse('order_update', kwargs={'pk':order.id}))
        self.assertEqual(response.status_code, 200)

        # form = OrderForm(order)
        # order.comment = 'new test'
        # order.save()

        response = self.client.post(reverse('order_update', kwargs={'pk':order.id}), 
            {'unique_identifier_for_order':order.unique_identifier_for_order,
            'customer':order.customer.id,
            'product': order.product.id,
            'comments':'new test'})

        # redirect to order list after update
        self.assertEqual(response.url, '/order/')
        self.assertEqual(response.status_code, 302)

    def test_update_view_update_existing_data_fail(self):
        order = Order.objects.all()[0]
        response = self.client.get(reverse('order_update', kwargs={'pk':order.id}))
        self.assertEqual(response.status_code, 200)

        # do not send customer data
        response = self.client.post(reverse('order_update', kwargs={'pk':order.id}), 
            {'product': order.product.id,
            'comments':'new test'})

        # redirect to order update page again when fail to update
        self.assertEqual(response.template_name,  ['order/order_edit.html'])
        self.assertEqual(response.status_code, 200)


    def test_create_view_url_exists_at_desired_location(self): 
        response = self.client.get('/order/create/') 
        self.assertEqual(response.status_code, 200)  
           
    def test_create_view_url_accessible_by_name(self):
        response = self.client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        response = self.client.get(reverse('order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order_create.html')


    def test_create_view_success(self):
        customer = Customer.objects.all()[0]
        product = Product.objects.all()[0]

        response = self.client.post(reverse('order_create'), 
            {
            'customer': customer.id,
            'product': product.id,
            'comments':'new test'})

        # redirect to order list after create an order
        self.assertEqual(response.url, '/order/')
        self.assertEqual(response.status_code, 302)

    def test_create_view_fail(self):

        product = Product.objects.all()[0]

        # post data without customer
        response = self.client.post(reverse('order_create'), 
            {
            'product': product.id,
            'comments':'new test'})

        # redirect to order create after fail to create
        self.assertEqual(response.template_name, ['order/order_create.html'])
        self.assertEqual(response.status_code, 200)


    def test_delete_view_url_exists_at_desired_location(self): 
        order = Order.objects.all()[0]
        response = self.client.get('/order/%s/delete'%(order.id)) 
        self.assertEqual(response.status_code, 200)  
           
    def test_delete_view_url_accessible_by_name(self):
        order = Order.objects.all()[0]
        response = self.client.get(reverse('order_delete',kwargs={'pk':order.id}))
        self.assertEqual(response.status_code, 200)

    def test_delete_view_uses_correct_template(self):
        order = Order.objects.all()[0]
        response = self.client.get(reverse('order_delete', kwargs={'pk':order.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/order_delete.html')


    def test_delete_view_successful(self):
        order = Order.objects.all()[0]
        response = self.client.post(reverse('order_delete', kwargs={'pk':order.id}))

        # redirect to order list after delete an order
        self.assertEqual(response.url, '/order/')
        self.assertEqual(response.status_code, 302)

    def test_delete_view_not_exist(self):
        response = self.client.post(reverse('order_delete', kwargs={'pk':10000000000}))

        # try to delete the record that does not exist
        # will show page not fould
        self.assertEqual(response.status_code, 404)



