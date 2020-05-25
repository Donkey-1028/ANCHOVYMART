from django.urls import path
from .views import test, InputRate

app_name = 'recommend'

urlpatterns = [
    path('test/', test, name='test'),
    path('input_rate/', InputRate.as_view(), name='input_rate'),

]