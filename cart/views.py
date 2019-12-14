from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cart

from shop.models import Product


@login_required
def cart_detail(request):
    """장바구니 세부목록 출력 위한 뷰."""
    try:
        products = Product.objects.filter(available=True)
        carts = get_list_or_404(Cart, user_id=request.user.id, product_id__in=products)
    except:
        product_total_price = 0
        carts = None
    else:
        """총금액 계산"""
        product_total_price = 0
        for i in range(len(carts)):
            product_total_price += carts[i].get_total_price()

    return render(request, 'cart/cart_detail.html', {'carts': carts,
                                                     'product_total_price': product_total_price})


@login_required
def add(request, product_slug):
    """장바구니에 해당 상품을 추가하기 위한 뷰"""
    product = get_object_or_404(Product, slug=product_slug)

    if request.method == 'GET':
        amount = request.GET.get('amount')
        if int(amount) > int(product.amount):
            """장바구니 담는 수량이 판매하는 수량보다 많을경우 못담게 하는 if문"""
            messages.warning(request, '판매하는 수량보다 더 높게 장바구니에 담으셨습니다.')
            return redirect('shop:product_detail', product.pk, product.slug)
        else:
            try:
                """요청한 유저 장바구니에 해당 상품이 있는지 get 한다."""
                cart = get_object_or_404(Cart, user_id=request.user.id, product=product)
            except:
                """만약 없을경우 새롭게 장바구니 데이터를 만들면서 수량 몇개를 장바구니에 보관할지
                입력받고 보관한다."""
                cart = Cart.objects.create(user_id=request.user.id, product_id=product.id, amount=amount)
                cart.save()
            else:
                """만약 있는경우라면 이미 있는 장바구니에 추가한 수량만큼 추가시킨다 ."""
                cart.amount += int(amount)
                cart.save()

    return redirect('cart:cart_detail')


@login_required
def delete(request, product_id):
    """장바구니의 특정 상품을 삭제하기 위한 뷰"""
    cart = get_object_or_404(Cart, user_id=request.user.id, product_id=product_id)
    cart.delete()

    try:
        cart = get_list_or_404(Cart, user_id=request.user.id)
    except:
        return render(request, 'cart/cart_detail.html')
    else:
        return redirect('cart:cart_detail')


@login_required
def clear(request):
    """장바구니를 비우기 위한 뷰"""
    cart = Cart.objects.filter(user_id=request.user.id).delete()

    return render(request, 'cart/cart_detail.html')
# Create your views here.
