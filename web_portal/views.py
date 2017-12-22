import json

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

from .models import Order, Customer, Product, Organization, Branch
from .utils import generate_context_data

# Create a new order


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):

    model = Order
    paginate_by = '10'
    context_object_name = 'order_list'
    queryset = Order.objects.all()
    template_name = 'order/order_list.html'


def sign_in(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if user and user.check_password(password):
                login(request, user)
                return redirect('/order')
            error = "Password is wrong"
        except ObjectDoesNotExist:
            error = "User name is wrong"
            pass

    return render(request, 'base/sign_in.html', {'error': error})


def sign_out(request):
    logout(request)
    return redirect('/login')
