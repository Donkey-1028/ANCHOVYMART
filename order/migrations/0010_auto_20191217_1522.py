# Generated by Django 2.1 on 2019-12-17 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20191216_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.Product'),
        ),
    ]
