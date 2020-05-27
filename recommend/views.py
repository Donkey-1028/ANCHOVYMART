from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.core.paginator import Paginator

from order.models import OrderProduct

from shop.models import Product

from .forms import RateForm


class InputRate(View):

    def get(self, request, order_product_pk):
        form = RateForm()
        order_product = OrderProduct.objects.get(id=order_product_pk)
        messages.warning(request, '평점의 범위를 1부터 5까지로 부여해주세요')
        return render(request, 'recommend/input_rate.html', {'form':form, 'order_product':order_product})

    def post(self, request, order_product_pk):
        order_product = OrderProduct.objects.get(id=order_product_pk)
        if request.method == 'POST':
            form = RateForm(request.POST or None)

            if form.is_valid():
                form.instance.user = self.request.user
                form.instance.order_product = order_product
                order_product.rated = True
                order_product.product.rated += form.instance.rate
                order_product.product.rate_count += 1
                order_product.product.save()
                order_product.save()
                form.save()
            else:
                form = RateForm()
                return redirect('recommend:input_rate', order_product_pk)

        return redirect('recommend:show_recommend_products')


class ShowRecommendProducts(View):

    def get(self, request, *args, **kwargs):
        if OrderProduct.objects.filter(user_id=self.request.user.id, rated=False):
            messages.warning(request, '평점을 부여하지 않은 상품들이 있습니다. 평점을 입력해주세요.')
            return redirect('recommend:show_unrated_products')
        elif OrderProduct.objects.filter(user_id=self.request.user.id):
            print('알고리즘처리')
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

class NonPersonalProducts(ListView):
    model = Product
    template_name = 'recommend/non_personal_products.html'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.all().order_by('-rate')[:6]

