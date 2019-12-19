from django.contrib import admin
from .models import *

import csv
from django.utils import timezone
from django.http import HttpResponse


def make_csv(modeladmin, request, queryset):
    """DB data로 CSV파일로 만드는 action"""
    now = timezone.now().day
    response = HttpResponse(content_type='text/csv')
    """파일 명은 현재날짜_order.csv"""
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(str(now)+'_order')
    response.write(u'\ufeff'.encode('utf-8')) # 한글 깨짐 방지
    writer = csv.writer(response)

    keys = []
    for key in queryset.values()[0].keys():
        """order의 key값들을 첫번째 줄에 저장."""
        if key == 'user_id' or key == 'created':
            """단 user_id, created일 경우에는 pass"""
            pass
        else:
            keys.append(key)
    keys.append('product')
    writer.writerow(keys)

    values = []
    for i in range(len(queryset)):
        passing = 1
        """넘어간 key값들의 value값도 pass하기 위한 수"""
        for value in queryset.values()[i].values():
            if passing is 2 or passing is 8:
                """passing이 2 이거나 8일경우, 즉 user_id이거나 created일경우 넘김"""
                passing += 1
            else:
                values.append(value)
                passing += 1

        """해당 order의 product들 또한 해당 csv파일에 추가하기 위함."""
        products = queryset[i].OrderProduct.all()
        product = ''
        for j in range(len(products)):
            """order에 연결된 product갯수만큼 for문, 그리고 해당 상품명(상품갯수), 를 저장후 리스트에 추가"""
            product += str(products[j].product.id) + '(' + str(products[j].amount) + '), '
        values.append(product)
        writer.writerow(values)
        values = []

    return response


make_csv.short_description = 'Make csv'


class OrderProductInline(admin.TabularInline):
    model = OrderProduct


class OrderManager(admin.ModelAdmin):
    list_display = ['id', 'user', 'buyer', 'address', 'price', 'created', 'status']
    list_filter = ['status', 'created']
    inlines = [OrderProductInline]
    actions = [make_csv]


class OrderTransactionManager(admin.ModelAdmin):
    list_display = ['order_id', 'imp_uid', 'merchant_uid', 'price', 'created', 'status']
    search_fields = ['order__id']


admin.site.register(Order, OrderManager)
admin.site.register(OrderTransaction, OrderTransactionManager)
# Register your models here.
