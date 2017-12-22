import json

from .models import Organization, Branch, Customer, Product


# Get available branchs for each organization and customers of each branch


def model_context_data(context, organizations, branches, customers):

    # use django ORM

    organization_array = {}
    for organization in organizations:
        organization_array[organization.pk] = [
            org[0] for org in organization.branch_set.all().values_list('pk')
        ]
    context['organization_array'] = organization_array

    branch_array = {}
    for branch in branches:
        branch_array[branch.pk] = [
            bran[0] for bran in branch.customer_set.all().values_list('pk')
        ]
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
