import random

from django.db import models
from django.urls import reverse

from django.core.exceptions import ValidationError

# Organization model


class Organization(models.Model):

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return "%s" % (self.name)

# Branch model


class Branch(models.Model):

    name = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return "%s" % (self.name)

    def clean(self):
        existing_records = Branch.objects.filter(
            organization=self.organization.pk)
        if existing_records:
            for record in existing_records:
                if record.name == self.name:
                    raise ValidationError(
                        {'organization':
                         ('An organization cannot have same branch name.')})

# Customer model


class Customer(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)

    class Meta:
        ordering = ['name']

    def clean(self):
        if Customer.objects.filter(email__iexact=self.email):
            raise ValidationError(
                {'email': ('Another customer register this email.')})

    def __str__(self):
        branch_name, organization_name = self.get_part_name()
        return "%s - %s - %s" % (self.name, branch_name, organization_name)

    def get_part_name(self):
        branch = Branch.objects.get(id=int(self.branch.pk))
        return branch.name, branch.organization.name

    @property
    def get_full_name(self):
        branch_name, organization_name = self.get_part_name()
        return "%s - %s - %s" % (self.name, branch_name, organization_name)


# Product model

class Product(models.Model):

    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return "%s" % (self.name)

# Order model


class Order(models.Model):

    # Generate code for order (unique_identifier_for_order)

    def generate_unique_value():
        chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
        unique_value = ''
        for c in range(8):
            unique_value += random.choice(chars)
        return unique_value

    unique_identifier_for_order = models.CharField(
        max_length=200,
        unique=True,
        default=generate_unique_value,
        editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comments = models.TextField()

    class Meta:
        ordering = ['unique_identifier_for_order']

    def get_absolute_url(self):
        return reverse('order_update', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s" % (self.unique_identifier_for_order)
