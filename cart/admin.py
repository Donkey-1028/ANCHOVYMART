from django.contrib import admin

from .models import *


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'amount']
    list_filter = ['product']


admin.site.register(Cart, CartAdmin)
# Register your models here.
