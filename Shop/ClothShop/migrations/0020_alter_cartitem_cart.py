# Generated by Django 4.2.6 on 2023-12-15 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ClothShop', '0019_remove_cartitem_order_alter_order_items_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ClothShop.cart'),
        ),
    ]