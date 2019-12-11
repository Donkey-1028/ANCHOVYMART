from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountsLogoutView.as_view(), name='logout'),
    path('register/', register, name='register')
]