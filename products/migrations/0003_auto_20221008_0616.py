# Generated by Django 3.2.5 on 2022-10-08 06:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discount',
            old_name='on_above_perchase',
            new_name='on_above_purchase',
        ),
        migrations.AddField(
            model_name='promocode',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='promocode',
            name='expirable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='promocode',
            name='expire_at',
            field=models.DateTimeField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='promocode',
            name='user_who_have_used',
            field=models.ManyToManyField(related_name='user_who_have_used', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='promocode',
            name='users',
            field=models.ManyToManyField(related_name='new_user_to_promo', to=settings.AUTH_USER_MODEL),
        ),
    ]
