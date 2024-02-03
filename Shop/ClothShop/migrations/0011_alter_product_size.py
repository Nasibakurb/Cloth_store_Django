# Generated by Django 4.2.6 on 2023-12-12 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClothShop', '0010_product_brand_product_color_product_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(choices=[('', ''), ('S', '42'), ('M', '44'), ('L', '46'), ('XL', '48'), ('XXL', '50'), ('XXXL', '52')], default='', max_length=100),
        ),
    ]
