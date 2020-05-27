import decimal

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone

from shop.models import Product

from .iamport import payments_prepare, find_transaction


class Order(models.Model):
    """주문서 개념의 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer = models.CharField('구매자', max_length=10)
    address = models.CharField('주소', max_length=100)
    """영수증에서 결제완료가 인증이 되면 주문서의 상태도 True로 전환"""
    status = models.BooleanField('결제 검증 상태', default=False)
    price = models.DecimalField('가격', max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField('전체 수량', default=0)
    created = models.DateTimeField('주문 날짜', auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.id)+self.buyer



class OrderProduct(models.Model):
    """주문서에 들어가는 상품 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """related_name을 설정하여 주문서에서 order.OrderProduct.all()로 접근 가능
    default값은 order.OrderProduct_set.all()"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='OrderProduct')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField('가격', max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField(default=1)

    rated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        return decimal.Decimal(self.price) * int(self.amount)



class OrderTransactionManager(models.Manager):
    def create_new_transaction(self, order, price):
        """주문서를 받아서 그 주문에 해당하는 고유의 merchant_uid 생성."""
        if not order:
            raise ValueError('주문 오류')

        merchant_created_uid = str(order.id) + order.buyer + str(timezone.now().date())
        "iamport에 merchant_uid와 가격을 미리 전달, 결제할 때 검증하는 과정"
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
        """iamport의 영수증을 가져오는 함수"""
        transaction = find_transaction(merchant_uid)
        if transaction['status'] == 'paid':
            """가져온 영수증이 있으면 해당 영수증 리턴"""
            return transaction
        else:
            return None


class OrderTransaction(models.Model):
    """주문서에 관한 영수증 개념의 모델"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='OrderTransaction')
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


def order_validation(sender, instance, created, *args, **kwargs):
    """DB영수증이 생성될때 iamport영수증과 맞는지 검증하는 함수"""
    if instance.imp_uid:
        """최초에 생성될때는 DB영수증에 imp_uid가 없고 결제가 완료된 후에
        DB영수증에 imp_uid를 생성해줌. 그래서 최초 생성될때는 pass로 넘어감"""
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
        raise ValueError('imp_uid 오류')


"""signals로 Ordertransaction이 생성될때 order_validation 함수 실행
sender 는 klass, instance는 해당하는 klass 정보"""
post_save.connect(order_validation, sender=OrderTransaction)
# Create your models here.
