# Generated by Django 4.2.6 on 2023-12-14 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClothShop', '0016_remove_cartitem_status_orderitem_alter_order_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='status',
            field=models.CharField(choices=[('processing', 'Обрабатывается'), ('shipped', 'Отправлен'), ('delivered', 'Доставлен'), ('returned', 'Возвращен'), ('return_request', 'Запрос на возврат')], default='processing', max_length=20),
        ),
    ]
