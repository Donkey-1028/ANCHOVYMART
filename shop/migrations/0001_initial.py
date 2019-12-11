# Generated by Django 2.1 on 2019-12-07 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=10, verbose_name='카테고리명')),
                ('meta_description', models.TextField(blank=True, verbose_name='설명')),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='슬러그')),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=10, verbose_name='상품명')),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='photo/', verbose_name='상품 이미지')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='가격')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='수량')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='슬러그')),
                ('available', models.BooleanField(default=True, verbose_name='구매가능여부')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Category')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together={('id', 'slug')},
        ),
    ]
