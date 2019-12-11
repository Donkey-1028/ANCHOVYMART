from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('카테고리명', max_length=10, db_index=True)

    """SEO을 위해 만드는 필드,
    구글 등 검색엔진에서 상품이 더 잘 검색되도록 하려면 여러가지 정보를
    제공해야 한다고 한다."""
    meta_description = models.TextField('설명', blank=True)

    """상품명을 이용해서 URL을 만드는 방식을 이용하기 위해 slug 필드도 사용한다.
    많은 블로그와 쇼핑몰에서 사용하는 방식이라고 한다.
    allow_unicode는 영문을 제외한 다른 언어도 값으로 사용할 수 있게 하는 옵션이다"""
    slug = models.SlugField('슬러그', max_length=100, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['-name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_products', args=[self.slug])


class Product(models.Model):
    name = models.CharField('상품명', max_length=10, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField('상품 이미지', upload_to='photo/')

    #price = models.PositiveIntegerField('가격', default=0)
    """해외나 화폐가 다른 국가에서 주문할 경우 보통은
    웹에서 해당국가에 해당하는 통화가치로 변경해서 표시한다고 한다.
    그러기 위해서 내부적으로 계산을 하는데 그렇기에 DecimalField를 사용한다고 한다.
    max_digits는 최대 자릿수, decimal_places는 소수자리수"""
    price = models.DecimalField('가격', max_digits=10, decimal_places=2)

    amount = models.PositiveIntegerField('수량', default=0)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField('슬러그', max_length=100, unique=True, allow_unicode=True, db_index=True)

    """재고가 없는 등 여러가지 요인으로 인해 구매가 가능하지 않더라고 하더라도
    쇼핑몰에서 해당 목록을 없애지 않고 홍보를 위해 냅두는 경우가 있다
    그럴 경우를 위해 만들었다"""
    available = models.BooleanField('구매가능여부', default=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created']
        """멀티 컬럼 색인 기능. id와 slug필드를 묶어서 색인하도록 하는 옵션"""
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

# Create your models here.
