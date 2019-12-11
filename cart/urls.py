from django.urls import path
from .views import *

app_name = 'cart'

urlpatterns = [
    path('cart_detail/', cart_detail, name='cart_detail'),
    path('add/<product_slug>/', add, name='cart_add'),
    path('delete/<int:product_id>/', delete, name='cart_delete'),
    path('clear/', clear, name='cart_clear'),
]