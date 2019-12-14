from django.urls import path
from .views import *

app_name = 'order'

urlpatterns = [
    path('cart_order_create/', cart_order_create, name='cart_order_create'),
    path('single_order_create/<product_slug>/<amount>/', single_order_create, name='single_order_create'),
    path('cart_order_create_ajax/', CartOrderCreateAjaxView.as_view(), name='cart_order_create_ajax'),
    path('merchant_create_ajax/', MerchantCreateAjaxView.as_view(), name='merchant_create_ajax'),

]
