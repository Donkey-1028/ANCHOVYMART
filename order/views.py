from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.views.generic.base import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import OrderCreateForm

from cart.models import Cart

@login_required
def cart_order_create(request):
    """주문서를 쓰기위한 뷰"""
    carts = get_list_or_404(Cart, user_id=request.user.id)
    carts_total_price = 0
    carts_amount = 0
    """주문하는 종합금액과 종합수량을 계산"""
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
            """장바구니에 있는 상품들로 OrderProduct를 생성."""
            OrderProduct.objects.create(
                user=request.user,
                order=order,
                product=cart.product,
                price=cart.product.price,
                amount=cart.amount,
            )

        return render(request, 'order/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'order/order_create.html', {'form': form, 'carts': carts,
                                                       'carts_total_price': carts_total_price,
                                                       'carts_amount': carts_amount
                                                       })


class CartOrderCreateAjaxView(LoginRequiredMixin, View):
    """iamport와 Ajax로 통신하기 위한 뷰,
    cart_order_create와 비슷하지만 cart_order_create에서 입력받은 form내용들을
    ajax를 통해 해당 뷰로 전송"""
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

            data = {
                'order_id': order.id,
                'price': order.price
            }
            return JsonResponse(data)
        else:
            raise ValueError('폼이 유효하지 않습니다')


class MerchantCreateAjaxView(LoginRequiredMixin, View):
    """ajax로 받은 데이터를 통해서 Merchant_id를 생성하기 위한 뷰"""
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        """decimal로 표현되어있는 price를 int형으로 변환"""
        final_price = round(float(order.price))

        try:
            merchant_uid = OrderTransaction.objects.create_new_transaction(
                order=order,
                price=final_price,
            )
        except:
            merchant_uid = None

        if merchant_uid is not None:
            data = {
                'merchant_id': merchant_uid
            }
            return JsonResponse(data)
        else:
            raise ValueError('merchant_uid 생성실패')


class OrderValidationAjaxView(LoginRequiredMixin, View):
    """iamport의 transaction과 db의 transaction이 일치하는지 검증하는 뷰"""
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        imp_id = request.POST.get('imp_id')
        merchant_uid = request.POST.get('merchant_id')
        price = request.POST.get('amount')


        try:
            transaction = OrderTransaction.objects.get(
                order=order,
                merchant_uid=merchant_uid,
                price=int(price)
            )
        except:
            transaction = None

        if transaction is not None:
            """imp_uid를 설정해주므로써 signals를 통해 연결되는 함수가
            검증을 진행시키기위한 조건을 만족시키게함."""
            transaction.imp_uid = imp_id
            transaction.status = True
            transaction.save()
            order.status = True
            order.save()

            """주문을 성공적으로 완료했을 경우 장바구니를 비움"""
            Cart.objects.filter(user_id=request.user.id).delete()

            data = {
                'done': True
            }

            return JsonResponse(data)
        else:
            raise ValueError('transaction 에러')


class OrderComplete(LoginRequiredMixin, View):
    """주문이 끝나면 사용되는 뷰"""
    def get(self, request, *args, **kwargs):
        """get으로 접근할 경우 주문에 대한 데이터만 출력"""
        order_id = kwargs['order_id']
        order = Order.objects.get(id=order_id)
        #order.OrderTransaction.all()[0].imp_uid 등등

        return render(request, 'order/order_created.html', {'order': order})

    def post(self, request, *args, **kwargs):
        """ajax로 post로 접근할 경우 주문한 수량만큼 DB에서 해당 품목의 수량을 빼는 뷰"""
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        if order.status is True:
            for i in range(len(order.OrderProduct.all())):
                """주문한 상품만큼 해당 상품 수량에서 빼기."""
                change = order.OrderProduct.all()[i].product
                change.amount -= order.OrderProduct.all()[i].amount
                change.save()

                """만약 구매한 물품의 재고가 0이 될 경우 판매 할수 없도록 만듬."""
                Product.objects.get(id=change.id).check_amount()

            data = {
                'change': True
            }
            return JsonResponse(data)
        else:
            return redirect('order:cart_order_create')


class OrderCheck(LoginRequiredMixin, View):
    """주문이 제대로 되었는지 사용자가 확인하는 뷰"""
    def get(self, request):
        orders = Order.objects.filter(user_id=request.user.id)
        fail = 0

        for i in range(len(orders)):
            """주문에 실패한 경우의 주문들의 갯수를 계산"""
            if orders[i].status is False:
                fail += 1

        return render(request, 'order/order_check.html', {'orders': orders, 'fail': fail})


class TransactionCheck(LoginRequiredMixin, View):
    """해당하는 주문에 대한 영수증을 사용자가 확인하기 위한 뷰"""
    def get(self, request, *args, **kwargs):
        """주문에 해당하는 영수증 가져오기"""
        transaction = get_object_or_404(OrderTransaction, order_id=kwargs['order_id'])
        """주문에 해당하는 품목들 가져오기"""
        order_product = get_list_or_404(OrderProduct, order_id=kwargs['order_id'])
        result = find_transaction(transaction.merchant_uid, transaction.price)

        return render(request, 'order/transaction_check.html', {'transaction': transaction,
                                                                'result': result,
                                                                'products': order_product})


class DeleteFailedOrder(LoginRequiredMixin, View):
    """주문에 실패한 주문들들 전부 삭제하는 뷰"""
    def get(self, request):
        Order.objects.filter(user_id=request.user.id, status=False).delete()

        return redirect('order:order_check')

# Create your views here.
