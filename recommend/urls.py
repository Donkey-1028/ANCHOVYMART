from django.urls import path
from .views import test

app_name = 'recommend'

urlpatterns = [
    path('test/', test, name='test'),
]