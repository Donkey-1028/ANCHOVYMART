from django.urls import path
from .views import  InputRate, ShowRecommendProducts, ShowUnratedProducts, NonPersonalProducts, PersonalProducts

app_name = 'recommend'

urlpatterns = [
    path('input_rate/<int:order_product_pk>', InputRate.as_view(), name='input_rate'),
    path('show_recommend_products/', ShowRecommendProducts.as_view(), name='show_recommend_products'),
    path('show_unrated_products/',ShowUnratedProducts.as_view(), name='show_unrated_products'),
    path('non_personal_products/', NonPersonalProducts.as_view(), name='non_personal_products'),
    path('personal_products/', PersonalProducts.as_view(), name='personal_products'),

]