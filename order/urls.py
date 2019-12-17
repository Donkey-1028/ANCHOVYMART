from django.urls import path
from .views import *

app_name = 'order'

urlpatterns = [
    path('cart_order_create/', cart_order_create, name='cart_order_create'),
    path('cart_order_create_ajax/', CartOrderCreateAjaxView.as_view(), name='cart_order_create_ajax'),
    path('merchant_create_ajax/', MerchantCreateAjaxView.as_view(), name='merchant_create_ajax'),
    path('order_validation_ajax/', OrderValidationAjaxView.as_view(), name='order_validation_ajax'),
    path('order_check/', OrderCheck.as_view(), name='order_check'),
    path('<order_id>/transaction_check/', TransactionCheck.as_view(), name='transaction_check'),
    path('order_delete/', DeleteFailedOrder.as_view(), name='order_delete'),
    path('order_complete/<order_id>', OrderComplete.as_view(), name='order_complete'),

]
