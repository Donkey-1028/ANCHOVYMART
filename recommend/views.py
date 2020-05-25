import numpy as np
import pandas as pd

from django.shortcuts import render
from order.models import OrderProduct

from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import NormalPredictor
from surprise import Reader


def test(request):
    a = np.array([[1,2],[3,4]])
    print(a)
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
"""

def surprise_test():
    ratings_dict = {'itemID': [1, 1, 1, 2, 2],
                    'userID': [9, 32, 2, 45, 'user_foo'],
                    'rating': [3, 2, 4, 3, 1]}
    df = pd.DataFrame(ratings_dict)
    # A reader is still needed but only the rating_scale param is requiered.
    reader = Reader(rating_scale=(1, 5))
    algo = SVD()
    # The columns must correspond to user id, item id and ratings (in that order).
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)

    # We can now use this dataset as we please, e.g. calling cross_validate
    cross_validate(algo, data, cv=2, verbose=True)
# Create your views here.
