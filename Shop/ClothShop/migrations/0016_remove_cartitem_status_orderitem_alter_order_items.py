# Generated by Django 4.2.6 on 2023-12-14 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ClothShop', '0015_remove_order_status_cartitem_status_order_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='status',
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(choices=[('processing', 'Обрабатывается'), ('shipped', 'Отправлен'), ('delivered', 'Доставлен'), ('returned', 'Возвращен'), ('return_request', 'Запрос на возврат')], default='processing', max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='ClothShop.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ClothShop.product')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orders', to='ClothShop.orderitem'),
        ),
    ]