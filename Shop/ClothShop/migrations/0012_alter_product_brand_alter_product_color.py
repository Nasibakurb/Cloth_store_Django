# Generated by Django 4.2.6 on 2023-12-12 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClothShop', '0011_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(choices=[('adidas', 'Адидас'), ('Nike', 'Найк')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(default='', max_length=25),
        ),
    ]
