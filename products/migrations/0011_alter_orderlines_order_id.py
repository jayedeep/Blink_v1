# Generated by Django 3.2.5 on 2022-10-14 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_orderlines_per_order_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlines',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='products.orders'),
        ),
    ]
