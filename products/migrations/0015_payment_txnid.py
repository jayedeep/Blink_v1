# Generated by Django 3.2.5 on 2022-10-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_delivery_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='txnId',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
