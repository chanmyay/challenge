from rest_framework import serializers

from .models import Order, Product, Customer


class OrderListSerializers(serializers.ModelSerializer):
    unique_identifier_for_order = serializers.CharField(max_length=8)
    customer = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    comments = serializers.CharField()

    class Meta:
        model = Order
        fields = ['unique_identifier_for_order', 'customer', 'product', 'comments']


class OrderSerializers(serializers.ModelSerializer):
    unique_identifier_for_order = serializers.CharField(max_length=8)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    comments = serializers.CharField()

    class Meta:
        model = Order
        fields = ('unique_identifier_for_order', 'customer', 'product','comments')


    def create(self, serializers):
        order = Order(unique_identifier_for_order=serializers.validated_data['unique_identifier_for_order'], 
                customer=serializers.validated_data['customer'], product=serializers.validated_data['product'], 
                comments=serializers.validated_data['comments'])
        order.save()
        context = {}
        context['unique_identifier_for_order'] = order.unique_identifier_for_order
        return context