import numpy as np
import pandas as pd

from django.shortcuts import render, redirect
from django.views.generic.base import View

from surprise import KNNBasic
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise import Reader

from order.models import OrderProduct
from .forms import RateForm

class InputRate(View):

    def get(self, request, *args, **kwargs):
        form = RateForm()
        return render(request, 'recommend/input_rate.html', {'form':form})

    def post(self, request, *args, **kwargs):
        order_product = OrderProduct.objects.get(id=206)
        print(order_product)
        if request.method == 'POST':
            form = RateForm(request.POST or None)

            if form.is_valid():
                form.instance.user = self.request.user
                form.instance.order_product = order_product
                form.save()
        return redirect('/')
"""
상품들마다 rate 측정할수 있게 페이지 만들기,
이미 평점이 등록된건 수정할 수도 있게 만들기.
"""

class ShowRatedProduct(View):

    def get(self, request, *args, **kwargs):

        pass
    pass

def test(request):
    content = OrderProduct.objects.filter(product_id=9)
    order_range = []
    for index, value in enumerate(content):
        order_range.append(value.order.id)
    content2 = OrderProduct.objects.filter(order_id__in=order_range)
    print(content2)
    return render(request, 'recommend/test.html', {'content':content2})

"""
주문서들로 협업필터링 돌려서 가장 나은 알고리즘 찾기
해당 알고리즘으로 어떻게 이용할건지 생각해보기.
> 평점 기능을 만들고
각각의 유저들은 orderproduct에 연결되는 평점테이블에 평점을 기록.
해당유저와 유사도가 가장 비슷한 유저를 찾고
그 사용자가 구매하지 않은것중 평점순서대로 추천.

하나 더 만들어서 단순히 가장 많은 평점을 가진것 추천

"""

def surprise_test():
    ratings_dict = {'itemID': [1, 1, 1, 2, 2, 3],
                    'userID': [9, 32, 2, 3, 45, 'user_foo'],
                    'rating': [3, 2, 4, 3, 1, 10]}
    print(ratings_dict)
    df = pd.DataFrame(ratings_dict)
    # A reader is still needed but only the rating_scale param is requiered.
    reader = Reader(rating_scale=(1, 5))
    algo = KNNBasic()
    # The columns must correspond to user id, item id and ratings (in that order).
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

    # We can now use this dataset as we please, e.g. calling cross_validate
    a = cross_validate(algo, data, cv=2, measures=['RMSE'], verbose=True)
    print(a)
# Create your views here.
