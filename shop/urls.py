from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns =[
    path('', product_category, name='all_products'),
    path('search', product_search, name='search'),
    path('<slug:slug>/', product_category, name='category_products'),
    path('<int:pk>/<product_slug>/', product_detail, name='product_detail'),
]