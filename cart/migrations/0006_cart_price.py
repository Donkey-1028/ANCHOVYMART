# Generated by Django 2.1 on 2019-12-08 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cart_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='가격'),
            preserve_default=False,
        ),
    ]
