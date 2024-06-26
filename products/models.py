import random

from django.db import models
from users.models import User, State, Employee
from django.core.validators import MaxValueValidator, MinValueValidator 
from datetime import datetime
from datetime import timedelta
from PIL import Image
from django.conf import settings

# Create your models here.
import uuid

from utils.helper_functions import get_voucher_discount
from django.utils.translation import gettext_lazy as _


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        if hasattr(self.model,'is_deleted'):
            return super().get_queryset().filter(is_deleted=False)
        else:
            return super().get_queryset()

class Warehouse(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    mobile_no=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    objects = SoftDeleteManager()


    def __str__(self):
        return self.name + " owned by " + self.owner.username
class Category(models.Model):
    category_name=models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return self.category_name

class Subcategory(models.Model):
    subcategory_name=models.CharField(max_length=50)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return self.subcategory_name

class AttributeName(models.Model):
    a_name=models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return self.a_name

class AttributeValue(models.Model):
    a_value=models.CharField(max_length=50)
    a_name=models.ForeignKey(AttributeName,on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return self.a_name.a_name +" - "+self.a_value


class Products(models.Model):
    p_name=models.CharField(max_length=50,blank=False,null=False)
    p_category=models.ForeignKey(Category, on_delete=models.CASCADE)
    p_subcategory=models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    p_created=models.DateField(auto_now_add=datetime.now)
    price=models.FloatField(validators=[MinValueValidator(1)])
    description=models.TextField()

    photo_1=models.ImageField(upload_to='products')
    photo_2=models.ImageField(upload_to='products')
    photo_3=models.ImageField(upload_to='products')
    photo_4=models.ImageField(upload_to='products',blank=True,null=True)
    photo_5=models.ImageField(upload_to='products',blank=True,null=True)
    photo_6=models.ImageField(upload_to='products',blank=True,null=True)

    product_maker = models.ForeignKey(User,on_delete=models.CASCADE,related_name='products')
    is_qa_verified = models.BooleanField(default=False)
    is_product_finest = models.BooleanField(default=True) # make it to false on product reject from Qa
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return self.p_name + " with "+ self.p_category.category_name
    
    def save(self, *args, **kwargs):
        super(Products, self).save(*args, **kwargs)
        imag1 = Image.open(self.photo_1.path)
        if imag1.width > 400 or imag1.height> 300:
            output_size = (400, 300)
            imag1.thumbnail(output_size)
            imag1.save(self.photo_1.path)
        imag2 = Image.open(self.photo_2.path)
        if imag2.width > 400 or imag2.height> 300:
            output_size = (400, 300)
            imag2.thumbnail(output_size)
            imag2.save(self.photo_2.path)
        imag3 = Image.open(self.photo_3.path)
        if imag3.width > 400 or imag3.height> 300:
            output_size = (400, 300)
            imag3.thumbnail(output_size)
            imag3.save(self.photo_3.path)

    def get_product_deals_of_date(self):
        deals_of_day_voucher = Vouchers.objects.filter(voucher_type='deals_of_day', products__id=self.id,is_deleted=False)
        return deals_of_day_voucher.first() or None

class ProductChangePriceAttributes(models.Model):
    attribute_values=models.ManyToManyField(AttributeValue)
    p_id= models.ForeignKey(Products,on_delete=models.CASCADE)
    price=models.FloatField(validators=[MinValueValidator(1)])
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return ','.join([str(attribute_value) for attribute_value in self.attribute_values.all()])


class Rates(models.Model):
    comment=models.CharField(max_length=50)
    rate = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    p_id= models.ForeignKey(Products,on_delete=models.CASCADE,blank=False,null=True)

    objects = SoftDeleteManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'p_id'], 
                name='unique product rate'
            )
        ]
    def __str__(self):
        return str(self.rate)+" by "+str(self.user)

class Stocks(models.Model):
    warehouse_id=models.ForeignKey(Warehouse,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    product_attributes=models.ForeignKey(ProductChangePriceAttributes,on_delete=models.CASCADE)
    total_qty=models.IntegerField(validators=[MinValueValidator(1)])
    left_qty=models.IntegerField(validators=[MinValueValidator(1)])
    on_alert_qty=models.IntegerField(validators=[MinValueValidator(1)])
    finished = models.BooleanField(default=False)

    objects = SoftDeleteManager()

    def __str__(self):
        return self.product_id.p_name + " At "+ self.warehouse_id.name + " with "+str(self.left_qty)

class Cart(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField(validators=[MinValueValidator(0)])
    price=models.FloatField(validators=[MinValueValidator(1)])
    selected_product_varient=models.CharField(max_length=100)
    vouchers = models.ForeignKey('Vouchers',on_delete=models.DO_NOTHING,null=True)

    def __str__(self):
        return str(self.user_id)+"'s carts "+ 'for'+ str(self.product_id.p_name)

class Checkout(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    address1=models.TextField()
    address2=models.TextField(blank=True,null=True)
    state=models.ForeignKey(State,on_delete=models.SET_NULL,null=True)
    city=models.CharField(max_length=100)
    zip=models.CharField(max_length=6)
    payment_type=models.CharField(max_length=50)

    def __str__(self):
        return str(self.user)+"'s Checkout "


class Vouchers(models.Model):
    choices = (
        ('on_above_purchase', 'On Above Purchase'),
        ('deals_of_day','Deals of Day'),
        ('product_together','Product Together'),
        ('promocode','Promocode'),
    )
    voucher_type = models.CharField(max_length=200,choices=choices)
    on_above_purchase = models.FloatField(null=True,blank=True) #on_above_purchase
    off_price = models.FloatField(null=True,blank=True) #on_above_purchase + #product_together +# promocode

    products = models.ManyToManyField(Products,null=True,blank=True,related_name='products') #deals_of_day + #product_together
    percent_off = models.FloatField(null=True,blank=True) #deals_of_day

    with_product = models.ForeignKey(Products,on_delete=models.DO_NOTHING,null=True,blank=True,related_name='with_product') #product_together

    promocode_name = models.CharField(max_length=100,null=True,blank=True) # promocode
    users=models.ManyToManyField(User,related_name='new_user_to_promo',null=True,blank=True) # promocode
    user_who_have_used=models.ManyToManyField(User,related_name='user_who_have_used',blank=True) # promocode
    created_at=models.DateTimeField(auto_now_add=datetime.now,null=True,blank=True) # promocode
    expirable=models.BooleanField(null=True,blank=True) # promocode
    expire_at=models.DateTimeField(null=True,blank=True)# promocode
    stop = models.BooleanField(null=True,blank=True,default=False) #on_above_purchase + #product_together +# promocode + #deals_of_day
    is_deleted = models.BooleanField(null=True,blank=True,default=False)
    objects = SoftDeleteManager()

    def get_name(self):
        if self.voucher_type == 'promocode':
            return "Promocode "+self.promocode_name
        else:
            if self.voucher_type == 'deals_of_day':
                return f"Buy Today and get {self.percent_off} off"
            if self.voucher_type == 'product_together':
                return self.with_product.name + " and get " + f"{self.off_price} Rs Off "
            if self.voucher.voucher_type == 'on_above_purchase':
                return f"Buy Any products above {self.on_above_purchase} Rs. and get {self.off_price}"

class Orders(models.Model):
    
    orderstatus=[
        ('order_prepared','Order Prepared'),
        ('order_confirm','Order Confirm'),
        ('order_cancel','Order Cancel'),
        ('order_delivering','Order Delivering'),
        ('order_shipped','Order Shipped'),
    ]
    orderid=models.CharField(max_length=50,default=uuid.uuid4)
    checkout=models.ForeignKey(Checkout,on_delete=models.DO_NOTHING)
    order_status=models.CharField(max_length=100,choices=orderstatus,default='order_confirm')
    created_at=models.DateTimeField(auto_now_add=datetime.now)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='buyer')
    payment_failed=models.BooleanField(default=True)
    amount=models.FloatField(validators=[MinValueValidator(0)])
    total_discount=models.FloatField(validators=[MinValueValidator(0)],default=0)
    vouchers = models.ForeignKey(Vouchers,on_delete=models.DO_NOTHING,null=True)

    def __str__(self):
        return str(self.orderid)

class OrderLines(models.Model):
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    qty=models.IntegerField(validators=[MinValueValidator(0)])
    unit_price=models.FloatField(validators=[MinValueValidator(1)])
    sub_total_amount=models.FloatField(validators=[MinValueValidator(0)])
    order_id=models.ForeignKey(Orders,on_delete=models.CASCADE,related_name='order')
    selected_product_varient = models.CharField(max_length=100)

class Delivery(models.Model):
    delivery_state = (('Confirm','Confirm'),
                      ('Started', 'Started'),
                      ('Delivering','Delivering'),
                      ('Shipped','Shipped'),)
    order = models.ForeignKey(Orders,on_delete=models.CASCADE)
    delivery_id=models.CharField(max_length=50,default=uuid.uuid4)
    delivery_person = models.ForeignKey(User,on_delete=models.CASCADE)
    state=models.CharField(max_length=100,choices=delivery_state,default='Confirm')
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=datetime.now)
    delivered_at=models.DateTimeField(blank=True,null=True)
    otp_code = models.CharField(max_length=6,blank=True,null=True)


    def save(self, *args, **kwargs):

        if self.pk:
            # If self.pk is not None then it's an update.
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            # This will get the current model state since super().save() isn't called yet.
            new = self  # This gets the newly instantiated Mode object with the new values.
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    if getattr(old, field_name) != getattr(new, field_name):
                        changed_fields.append(field_name)
                except Exception as ex:  # Catch field does not exist exception
                    pass
            kwargs['update_fields'] = changed_fields
        super().save(*args, **kwargs)

class OtpModel(models.Model):
    otp_number=models.CharField(max_length=6)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    verified=models.BooleanField(default=False)
    times=models.IntegerField(default=1)
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=datetime.now)
    payment_method=models.CharField(max_length=100,choices=[('Online','Online'),('Offline','Offline')])
    status=models.CharField(max_length=100,choices=(('Success','Success'),('Pending','Pending'),('Cancel','Cancel')))
    txnId=models.CharField(max_length=150,null=True,blank=True)

class Transaction(models.Model):
    PaymentStatus = [
        ('Success',"Success"),
        ("Failure","Failure"),
        ("Pending", "Pending")
    ]

    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = models.CharField(
        _("Payment Status"),
        default="Pending",
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Transaction Order ID"), max_length=40, null=False, blank=False
    )
    transaction_payment_id = models.CharField(
        _("Transaction Payment ID"), max_length=36, null=True, blank=True
    )
    signature_id = models.CharField(
        _("Transaction Signature ID"), max_length=128, null=True, blank=True
    )

    def __str__(self):
        return f"{self.id}-{self.status}"
