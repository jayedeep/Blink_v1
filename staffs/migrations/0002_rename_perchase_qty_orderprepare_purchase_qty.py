# Generated by Django 4.0.8 on 2023-09-26 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staffs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderprepare',
            old_name='perchase_qty',
            new_name='purchase_qty',
        ),
    ]
