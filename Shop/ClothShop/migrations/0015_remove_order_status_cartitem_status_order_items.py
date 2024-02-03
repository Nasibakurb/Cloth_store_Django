# Generated by Django 4.2.6 on 2023-12-14 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClothShop', '0014_product_max_price_product_min_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='status',
            field=models.CharField(choices=[('processing', 'Обрабатывается'), ('shipped', 'Отправлен'), ('delivered', 'Доставлен'), ('returned', 'Возвращен'), ('return_request', 'Запрос на возврат')], default='processing', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='ClothShop.cartitem'),
        ),
    ]