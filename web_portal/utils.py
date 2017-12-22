import random
import itertools
import json

from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from .models import Organization, Branch, Customer, Product


# Get available branchs for each organization and customers of each branch


def model_context_data(context, organizations, branches, customers):

    organization_array = {}
    for organization in organizations:
        organization_array[organization.pk] = [
            branch.pk for branch in branches
            if branch.organization.pk == organization.pk]
    context['organization_array'] = organization_array

    branch_array = {}
    for branch in branches:
        branch_array[branch.pk] = [
            customer.pk for customer in customers
            if customer.branch.pk == branch.pk]
    context['branch_array'] = branch_array
    return context


# Generate context data for new Order PAGE

def generate_context_data(context):
    organizations = Organization.objects.all()
    branches = Branch.objects.all()
    customers = Customer.objects.all()
    context['organizations'] = organizations
    context['branches'] = branches
    context['customers'] = customers
    context['products'] = Product.objects.all()
    context = model_context_data(context, organizations, branches, customers)
    return context

# Generate context data for new Order API


def generate_context_data_values(context):

    organizations = Organization.objects.all()
    branches = Branch.objects.all()
    customers = Customer.objects.all()
    products = Product.objects.all()

    context['organizations'] = list(organizations.values('pk', 'name'))
    context['branches'] = list(branches.values('pk', 'name'))
    context['customers'] = [
        {'pk': customer.pk, 'name': customer.get_full_name}
        for customer in customers]
    context['products'] = list(products.values('pk', 'name'))
    context = model_context_data(context, organizations, branches, customers)
    return context
