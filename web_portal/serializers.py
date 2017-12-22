from rest_framework import serializers

from .models import Order, Product, Customer


class OrderListSerializers(serializers.ModelSerializer):
    unique_identifier_for_order = serializers.CharField(max_length=8, read_only=True)
    customer = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    comments = serializers.CharField()

    class Meta:
        model = Order
        fields = ['unique_identifier_for_order',
                  'customer', 'product', 'comments']


class OrderSerializers(serializers.ModelSerializer):
    unique_identifier_for_order = serializers.CharField(max_length=8, read_only=True)
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all())
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())
    comments = serializers.CharField()

    class Meta:
        model = Order
        fields = ('unique_identifier_for_order',
                  'customer', 'product', 'comments')
