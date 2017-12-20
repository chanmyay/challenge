import random
import itertools
import json

from django.core.exceptions import ObjectDoesNotExist

from .models import Organization, Branch, Customer, Product


# Generate code for order (unique_identifier_for_order)

def generate_unique_value():
    chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    unique_value = ''
    for c in range(8):
        unique_value += random.choice(chars)
    return unique_value

# Get available branchs for each organization
# we can use two options (data map or query)
# data map ( one query will get all branchs and map with organization)
# query ( will make a query for each organization )

def model_organization_data():
    context = {}
    organizations = Organization.objects.all()
    for organization in organizations:
        try:
            branchs = Branch.objects.filter(organization=organization.id)
            context[organization.id] = [branch.id for branch in branchs]
        except ObjectDoesNotExist:
            pass
    return context

# Get available customers for each branch
# we can use two options (data map or query)
# data map ( one query will get all customers and map with branch)
# query ( will make a query for each branch )

def model_branch_data():
    context = {}
    branchs = Branch.objects.all()
    for branch in branchs:
        try:
            customers = Customer.objects.filter(branch=branch.id)
            context[branch.id] = [customer.id for customer in customers]
        except ObjectDoesNotExist:
            pass
    return context


# Generate context data for new Order PAGE

def generate_context_data(context):
    context['organizations'] = Organization.objects.all()
    context['branches'] = Branch.objects.all()
    context['customers'] = Customer.objects.all()
    context['products'] = Product.objects.all()
    organization_array = model_organization_data()
    branch_array = model_branch_data()
    context['organization_array'] =  json.dumps(organization_array)
    context['branch_array'] =  json.dumps(branch_array)
    return context

# Generate context data for new Order API

def generate_context_data_values(context):
    context['organizations'] = list(Organization.objects.all().values('name'))
    context['branches'] = list(Branch.objects.all().values('name'))
    context['customers'] = list(Customer.objects.all().values('name'))
    context['products'] = list(Product.objects.all().values('name'))
    organization_array = model_organization_data()
    branch_array = model_branch_data()
    context['organization_array'] =  str(organization_array)
    context['branch_array'] =  str(branch_array)
    return context