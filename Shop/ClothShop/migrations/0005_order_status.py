# Generated by Django 4.2.6 on 2023-12-10 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClothShop', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'Обрабатывается'), ('shipped', 'Отправлен'), ('delivered', 'Доставлен'), ('returned', 'возвращен')], default='processing', max_length=20),
        ),
    ]
