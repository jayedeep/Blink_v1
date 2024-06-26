# Generated by Django 4.0.8 on 2024-01-06 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications_app', '0004_remove_notification_contact_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='delivery',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='for_admin',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='for_customer',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='is_checked',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='prepare_order',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='sent',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='user_order',
        ),
        migrations.AddField(
            model_name='notification',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='receiver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='received_notifications', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='related_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sent_notifications', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(),
        ),
    ]
