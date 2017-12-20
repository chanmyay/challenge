from django import forms
from .models import Order, Customer, Product


class OrderForm(forms.Form):

    unique_identifier_for_order = forms.CharField()
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    comments = forms.CharField( widget=forms.Textarea )

    class Meta: 
        model = Order
        fields = ['unique_identifier_for_order','product','product','comments']