from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug'
    ]

    """prepopulated_fields옵션은 slug필드에 name으로 들어오는 값을 자동으로
    채워주는 역할을 하는 옵션이다."""
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'category', 'price', 'amount', 'available','rated', 'created'
    ]
    prepopulated_fields = {'slug': ('name',)}

    """list_editable 옵션을 이용해서 admin사이트 목록에서도 해당되는 값들을 바로바로 변경할 수 있음"""
    list_editable = ['price', 'amount', 'available']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

# Register your models here.
