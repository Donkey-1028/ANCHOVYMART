from django.db import models
from django.contrib.auth.models import User

from shop.models import Product

"""상품의 가격이 DecimalField이기 때문에 전체가격도 Decimal로 표현하기 위해 임포트"""
import decimal


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')

    amount = models.PositiveIntegerField('수량', default=1)


    def __str__(self):
        return self.user.username

    """해당 카트에서 전체 금액이 얼마인지 리턴하는 함수."""
    def get_total_price(self):
        return decimal.Decimal(self.product.price) * int(self.amount)

# Create your models here.
