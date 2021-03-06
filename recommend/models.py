from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

from order.models import OrderProduct

class Rate(models.Model):
    order_product = models.OneToOneField(OrderProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate= models.PositiveIntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return self.order_product.product.name + '/' +str(self.rate) + '/' + str(self.user)
# Create your models here.
