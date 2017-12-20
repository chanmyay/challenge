import json

from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Order, Customer, Product, Organization, Branch
from .utils import generate_unique_value, generate_context_data
from .forms import OrderForm

# Create a new order

class OrderCreate(CreateView):

    model = Order
    form_class = OrderForm
    template_name = 'order/order_create.html'
    success_url = '/order/'
    fields = '__all__'

    def get_context_data(self,**kwargs):
        context = {}
        context = generate_context_data(context)
        return context

    def post(self, request, *args, **kwargs):

        if not request.POST._mutable:
            request.POST._mutable = True
        request.POST['unique_identifier_for_order'] = generate_unique_value()
        form = OrderForm(request.POST)
        if form.is_valid():
            form.clean()
            order = Order.objects.create(
                unique_identifier_for_order=form.cleaned_data.get('unique_identifier_for_order'), 
                customer=form.cleaned_data.get('customer'), 
                product=form.cleaned_data.get('product'), 
                comments=form.cleaned_data.get('comments'))
            order.save()
            return redirect('order_list')
        else:
            return redirect('order_create')

# View / Edit the existing order

class OrderUpdate(DetailView):

    model = Order
    form_class = OrderForm
    template_name = 'order/order_edit.html'
    success_url = '/order/'

    def get_context_data(self,**kwargs):
        order = super().get_object()
        context = super().get_context_data(**kwargs)
        context['comments'] = order.comments
        context['selected_organization'] = Branch.objects.get(id=order.customer.branch.id).organization.id
        context['selected_branch'] = order.customer.branch.id 
        context['selected_customer'] = order.customer.id
        context['selected_product'] = order.product.id
        context['order_name'] = order.unique_identifier_for_order
        context = generate_context_data(context)
        return context

    def post(self, request, *args, **kwargs):

        if not request.POST._mutable:
            request.POST._mutable = True
        self.object = self.get_object()
        request.POST['unique_identifier_for_order'] = self.object.unique_identifier_for_order
        
        form = OrderForm(request.POST)
        if form.is_valid():
            form.clean()
            self.object.product = form.cleaned_data.get('product')
            self.object.customer = form.cleaned_data.get('customer')
            self.object.comments = form.cleaned_data.get('comments')
            self.object.save()
            return redirect('order_list')
        else:
            print(form.errors)
            return redirect('order_update', self.object.id)

# Delete the existing order

class OrderDelete(DeleteView):

    model = Order
    template_name = 'order/order_delete.html'
    success_url = '/order/'

    def get_context_data(self,**kwargs):
        order = super().get_object()
        context = super().get_context_data(**kwargs)
        context['order'] = order
        return context

# Retrieve all ordes

class OrderList(ListView):

    model = Order
    paginate_by='10'
    context_object_name = 'order_list'
    queryset = Order.objects.all()
    template_name = 'order/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context