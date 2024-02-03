# Generated by Django 4.2.6 on 2023-12-15 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClothShop', '0018_cartitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='order',
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='ClothShop.cartitem'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
