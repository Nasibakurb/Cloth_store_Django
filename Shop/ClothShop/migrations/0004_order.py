# Generated by Django 4.2.6 on 2023-12-07 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClothShop', '0003_cart_cartitem_cart_products_cart_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('card_number', models.CharField(max_length=16)),
                ('expiration_date', models.CharField(max_length=5)),
                ('cvv', models.CharField(max_length=3)),
            ],
        ),
    ]