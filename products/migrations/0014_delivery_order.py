# Generated by Django 3.2.5 on 2022-10-16 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_delivery_delivered_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='order',
            field=models.ForeignKey(default=16, on_delete=django.db.models.deletion.CASCADE, to='products.orders'),
            preserve_default=False,
        ),
    ]
