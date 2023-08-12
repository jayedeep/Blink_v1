# Generated by Django 4.0.8 on 2022-10-19 06:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0015_payment_txnid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('sent', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_buyer', to=settings.AUTH_USER_MODEL)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.delivery')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_seller', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
