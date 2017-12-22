from django.contrib import admin

from .models import Organization, Branch, Customer, Product, Order

admin.site.register(Organization)
admin.site.register(Branch)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
