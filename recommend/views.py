from django.shortcuts import render
from order.models import OrderProduct


def test(request):
    content = OrderProduct.objects.filter(product_id=9)
    order_range = []
    for index, value in enumerate(content):
        order_range.append(value.order.id)
    content2 = OrderProduct.objects.filter(order_id__in=order_range)
    print(content2)
    return render(request, 'recommend/test.html', {'content':content2})
# Create your views here.
