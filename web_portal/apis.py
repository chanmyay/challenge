import json

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Order
from .serializers import OrderListSerializers, OrderSerializers
from .utils import generate_context_data_values

# Order list API


class OrderListAPI(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializers

# Order create API


class OrderCreateAPI(generics.GenericAPIView):
    serializer_class = OrderSerializers

    def get(self, request, *args, **kwargs):
        context = generate_context_data_values({})
        data = json.dumps(context)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        order_serializer = OrderSerializers(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            return Response(order_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
