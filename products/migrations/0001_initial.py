# Generated by Django 4.0.8 on 2023-08-12 12:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_value', models.CharField(max_length=50)),
                ('a_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.attributename')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address1', models.TextField()),
                ('address2', models.TextField(blank=True, null=True)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=6)),
                ('payment_type', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deals_of_day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_price', models.FloatField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('on_above_purchase', models.FloatField()),
                ('percent_off', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.CharField(default=uuid.uuid4, max_length=50)),
                ('order_status', models.CharField(choices=[('                                                                                  q', 'Order Not Paid'), ('order_confirm', 'Order Confirm'), ('order_cancel', 'Order Cancel'), ('order_delivering', 'Order Delivering'), ('order_shipped', 'Order Shipped')], default='order_not_confirm', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment_failed', models.BooleanField(default=True)),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.checkout')),
                ('created_seller', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='seller', to=settings.AUTH_USER_MODEL)),
                ('deals_of_day', models.ManyToManyField(blank=True, null=True, to='products.deals_of_day')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.discount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='buyer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=50)),
                ('p_created', models.DateField(auto_now_add=True)),
                ('ingredience', models.CharField(max_length=500)),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField()),
                ('photo_1', models.ImageField(upload_to='products')),
                ('photo_2', models.ImageField(upload_to='products')),
                ('photo_3', models.ImageField(upload_to='products')),
                ('photo_4', models.ImageField(blank=True, null=True, upload_to='products')),
                ('photo_5', models.ImageField(blank=True, null=True, upload_to='products')),
                ('photo_6', models.ImageField(blank=True, null=True, upload_to='products')),
                ('p_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_name', models.CharField(max_length=50)),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('mobile_no', models.CharField(max_length=100)),
                ('name_of_shop', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stocks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_qty', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('left_qty', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('on_alert_qty', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('stock_day', models.DateField(auto_now_add=True)),
                ('finished', models.BooleanField(default=False)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.store')),
            ],
        ),
        migrations.CreateModel(
            name='Rates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=50)),
                ('rate', models.PositiveIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('p_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promocode', models.CharField(default=uuid.uuid4, max_length=50)),
                ('name_of_code', models.CharField(max_length=50)),
                ('discount_price', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expirable', models.BooleanField(default=True)),
                ('expire_at', models.DateTimeField()),
                ('user_who_have_used', models.ManyToManyField(related_name='user_who_have_used', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='new_user_to_promo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='p_subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.subcategory'),
        ),
        migrations.CreateModel(
            name='ProductChangePriceAttributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('attribute_values', models.ManyToManyField(to='products.attributevalue')),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('payment_method', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('txnId', models.CharField(blank=True, max_length=150, null=True)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.orders')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OtpModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_number', models.CharField(max_length=6)),
                ('varified', models.BooleanField(default=False)),
                ('times', models.IntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderLines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('per_order_amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='products.orders')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_id', models.CharField(default=uuid.uuid4, max_length=50)),
                ('state', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.orders')),
            ],
        ),
        migrations.AddField(
            model_name='deals_of_day',
            name='p_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_product', to='products.products'),
        ),
        migrations.AddField(
            model_name='deals_of_day',
            name='with_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='with_product', to='products.products'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('selected_product_varient', models.CharField(max_length=100)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='rates',
            constraint=models.UniqueConstraint(fields=('user', 'p_id'), name='unique product rate'),
        ),
    ]
