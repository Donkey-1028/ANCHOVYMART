from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from .models import *


def product_category(request, slug=None):
    """ 제품을 출력하기 위한 뷰,
    슬러그가 없을시 모든 제품을 출력"""
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    """상품들을 3개씩만 출력하기 위해 paginator 사용"""
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    if slug:
        """슬러그가 있을시 해당 슬러그에 해당하는 제품만 출력"""
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)

        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)

    return render(request, 'shop/list.html', {'category': category,
                                              'categories': categories,
                                              'contacts': contacts,
                                              'paginator': paginator})


def product_detail(request, pk, product_slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, pk=pk, slug=product_slug)
    product.get_rate()
    return render(request, 'shop/product_detail.html', {'product': product, 'categories': categories})


def product_search(request):
    """제품 검색을 위한 뷰"""
    categories = Category.objects.all()

    if request.method == 'GET':
        schWord = request.GET.get('search_word')

        search_list = Product.objects.filter(Q(name__icontains=schWord), available=True)

        if not search_list.exists():
            messages.warning(request, schWord+'에 해당하는 검색결과가 없습니다.')
            return redirect('shop:all_products')

        paginator = Paginator(search_list, 3)
        page = request.GET.get('page')
        contacts = paginator.get_page(page)

        return render(request, 'shop/list.html', {'categories': categories,
                                                  'contacts': contacts,
                                                  'paginator': paginator})
# Create your views here.
