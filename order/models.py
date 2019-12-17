import decimal

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone

from shop.models import Product

from .iamport import payments_prepare, find_transaction


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.CharField('구매자', max_length=10)
    address = models.CharField('주소', max_length=100)
    status = models.BooleanField('결제 검증 상태', default=False)
    price = models.DecimalField('가격', max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField('전체 수량', default=0)
    created = models.DateTimeField('주문 날짜', auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.id)+self.buyer



class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='OrderProduct')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField('가격', max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        return decimal.Decimal(self.price) * int(self.amount)


class OrderTransactionManager(models.Manager):
    def create_new_transaction(self, order, price):
        if not order:
            raise ValueError('주문 오류')

        merchant_created_uid = str(order.id) + order.buyer + str(timezone.now().date())

        payments_prepare(merchant_created_uid, price)

        transaction = self.model(
            order=order,
            merchant_uid=merchant_created_uid,
            price=price
        )

        try:
            transaction.save()
        except Exception as e:
            print('저장 오류', e)

        return transaction.merchant_uid

    def get_transaction(self, merchant_uid):
        transaction = find_transaction(merchant_uid)
        if transaction['status'] == 'paid':
            return transaction
        else:
            return None


class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    merchant_uid = models.CharField(max_length=100, null=True, blank=True)
    imp_uid = models.CharField(max_length=100, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    status = models.BooleanField('결제 상태', default=False)

    objects = OrderTransactionManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.order.id)

    def check_status(self):
        if self.status is True:
            return '결제완료'
        else:
            return '결제보류'


def order_validation(sender, instance, created, *args, **kwargs):
    if instance.imp_uid:
        iamport_transaction = OrderTransaction.objects.get_transaction(
            merchant_uid=instance.merchant_uid
        )

        merchant_uid = iamport_transaction['merchant_uid']
        imp_id = iamport_transaction['imp_uid']
        price = iamport_transaction['price']

        db_transaction = OrderTransaction.objects.filter(
            merchant_uid=merchant_uid,
            imp_uid=imp_id,
            price=price
        ).exists()

        if not iamport_transaction or not db_transaction:
            raise ValueError('결제 검증 오류')
    else:
        pass


post_save.connect(order_validation, sender=OrderTransaction)
# Create your models here.