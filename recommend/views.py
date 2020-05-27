from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.contrib import messages

from order.models import OrderProduct

from .forms import RateForm


class InputRate(View):

    def get(self, request, order_product_pk):
        form = RateForm()
        order_product = OrderProduct.objects.get(id=order_product_pk)
        return render(request, 'recommend/input_rate.html', {'form':form, 'order_product':order_product})

    def post(self, request, order_product_pk):
        order_product = OrderProduct.objects.get(id=order_product_pk)
        if request.method == 'POST':
            form = RateForm(request.POST or None)

            if form.is_valid():
                form.instance.user = self.request.user
                form.instance.order_product = order_product
                form.save()
                order_product.rated = True
                order_product.save()

        return redirect('recommend:show_recommend_products')
"""
상품들마다 rate 측정할수 있게 페이지 만들기,
이미 평점이 등록된건 수정할 수도 있게 만들기.
"""

class ShowRecommendProducts(View):

    def get(self, request, *args, **kwargs):
        if OrderProduct.objects.filter(user_id=self.request.user.id, rated=False):
            messages.warning(request, '평점을 부여하지 않은 상품들이 있습니다. 평점을 입력해주세요.')
            return redirect('recommend:show_unrated_products')
        else:
            print('all')
        return redirect('/')

class ShowUnratedProducts(ListView):
    model = OrderProduct
    template_name = 'recommend/show_unrated_products.html'

    def get_queryset(self):
        return OrderProduct.objects.filter(user_id=self.request.user.id, rated=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = len(OrderProduct.objects.filter(user_id=self.request.user.id, rated=False))
        return context



