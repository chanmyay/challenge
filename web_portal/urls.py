from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from .views import OrderCreate, OrderUpdate, OrderDelete, OrderList
from .apis import OrderListAPI, OrderCreateAPI

urlpatterns = [

    # WEB PAGE
    path('order/', OrderList.as_view(), name='order_list'),
    path('order/create/', OrderCreate.as_view(), name='order_create'),
    path('order/<slug:pk>/edit', OrderUpdate.as_view(), name='order_update'),
    path('order/<slug:pk>/delete', OrderDelete.as_view(), name='order_delete'),

    # REST FRAMEWORK JWT
    path('token_get/', obtain_jwt_token),
    path('token_verify/', verify_jwt_token),

    # WEB SERVICE / API
    path('api/order_list', OrderListAPI.as_view(), name='api_order_list'),
    path('api/order_create', OrderCreateAPI.as_view()),
    
]