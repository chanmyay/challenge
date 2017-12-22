import json

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse

from .models import Order, Customer, Product, Organization, Branch
from .utils import generate_context_data

# Create a new order


class OrderCreate(CreateView):

    model = Order
    template_name = 'order/order_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('order_list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context = generate_context_data(context)
        return context

# View / Edit the existing order


class OrderUpdate(UpdateView):

    model = Order
    # form_class = OrderForm
    template_name = 'order/order_edit.html'
    fields = ['customer', 'product', 'comments']

    def get_success_url(self):
        return reverse('order_list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['selected_organization'] = Branch.objects.get(
            id=self.object.customer.branch.pk).organization.pk
        context['selected_branch'] = self.object.customer.branch.pk
        context['selected_customer'] = self.object.customer.pk
        context['selected_product'] = self.object.product.pk
        context = generate_context_data(context)
        return context

# Delete the existing order


class OrderDelete(DeleteView):

    model = Order
    template_name = 'order/order_delete.html'

    def get_success_url(self):
        return reverse('order_list')

    def get_context_data(self, **kwargs):
        order = super().get_object()
        context = super().get_context_data(**kwargs)
        context['order'] = order
        return context

# Retrieve all ordes


class OrderList(ListView):

    model = Order
    paginate_by = '2'
    context_object_name = 'order_list'
    queryset = Order.objects.all()
    template_name = 'order/order_list.html'
