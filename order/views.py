from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views.generic.base import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from cart.models import Cart
from shop.models import Product

from .models import *
from .forms import OrderCreateForm


def cart_order_create(request):
    carts = get_list_or_404(Cart, user_id=request.user.id)
    carts_total_price = 0
    carts_amount = 0
    for i in range(len(carts)):
        carts_total_price += carts[i].get_total_price()
        carts_amount += carts[i].amount

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = request.user.id
            order.price = carts_total_price
            order.amount = carts_amount
            order.save()

        for cart in carts:
            OrderProduct.objects.create(
                user=request.user,
                order=order,
                product=cart.product,
                price=cart.product.price,
                amount=cart.amount,
            )

        Cart.objects.filter(user_id=request.user.id).delete()

        return render(request, 'order/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/order_create.html', {'form': form, 'carts': carts,
                                                       'carts_total_price': carts_total_price,
                                                       'carts_amount': carts_amount
                                                       })


def single_order_create(request, product_slug, amount):
    product = get_object_or_404(Product, slug=product_slug)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = request.user.id
            order.save()

        OrderProduct.objects.create(
            user=request.user,
            order=order,
            product=product,
            price=product.price,
            amount=int(amount)
        )
        return render(request, 'order/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'order/order_create.html', {'form': form})


class CartOrderCreateAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        available_products = Product.objects.filter(available=True)
        carts = get_list_or_404(Cart, user_id=request.user.id, product_id__in=available_products)

        carts_total_price = 0
        carts_amount = 0
        for i in range(len(carts)):
            carts_total_price += carts[i].get_total_price()
            carts_amount += carts[i].amount

        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = request.user.id
            order.price = carts_total_price
            order.amount = carts_amount
            order.save()

            for cart in carts:
                OrderProduct.objects.create(
                    order=order,
                    user=request.user,
                    product=cart.product,
                    price=cart.product.price,
                    amount=cart.amount
                )

            Cart.objects.filter(user_id=request.user.id, product_id__in=available_products).delete()

            data = {
                'order_id': order.id,
                'price': order.price
            }

            print('CartOrderCreateAjaxView성공@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            return JsonResponse(data)
        else:
            print('CartOrderCreateAjaxView실패@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            return JsonResponse({}, status=401)


class SingleOrderCreateAjaxView(LoginRequiredMixin, View):
    product_slug = 'product_slug'
    amount = 'amount'

    def post(self, request, product_slug, amount, *args, **kwargs):
        product = get_object_or_404(Product, slug=product_slug)
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = request.user.id
            order.save()

            OrderProduct.objects.create(
                order=order,
                user=request.user,
                product=product,
                price=product.price,
                amount=int(amount)
            )

            data = {
                'order_id': order.id
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

class MerchantCreateAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        price = request.POST.get('price')

        try:
            merchant_uid = OrderTransaction.objects.create_new_transaction(
                order=order,
                amount=price,
            )
        except:
            merchant_uid = None

        if merchant_uid is not None:
            print(merchant_uid)
            data = {
                'merchant_id': merchant_uid
            }
            print(data)
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)

# Create your views here.
