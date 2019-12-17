from django.contrib import admin
from .models import *


class OrderManager(admin.ModelAdmin):
    list_display = ['user', 'buyer', 'address', 'price']


class OrderProductManager(admin.ModelAdmin):
    list_display = ['user', 'order', 'product']


admin.site.register(Order, OrderManager)
admin.site.register(OrderProduct, OrderProductManager)
admin.site.register(OrderTransaction)
# Register your models here.
