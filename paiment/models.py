from chargily_epay_django.models import AnonymPayment, FakePaymentMixin
from django.urls import reverse
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from django.utils.translation import gettext_lazy as _
from books.models import Book
# Create your models here.


class State(models.Model):
    state_name = models.CharField(verbose_name="State Name", max_length=50)
    delivery_price = models.PositiveIntegerField(verbose_name="Delivery Price")
    state_date_add = models.DateTimeField(
        auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'الولاية'
        verbose_name_plural = 'الولايات'

    def __str__(self):
        return self.state_name


class AddresShiping(models.Model):
    user = models.ForeignKey(
        "users.User", verbose_name="user", on_delete=models.CASCADE, blank=True)
    stats = models.ForeignKey(
        State, verbose_name="state", on_delete=models.CASCADE)
    phone_number = models.CharField(
        verbose_name="Phone Number", max_length=10)
    address_complete = models.CharField(
        verbose_name="Address Complete", max_length=150)
    postal_code = models.CharField(
        verbose_name="Postal Code", max_length=10)
    city = models.CharField(
        verbose_name="city", max_length=100, blank=True)
    addres_shiping_date_add = models.DateTimeField(
        auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'عنوان الشحن'
        verbose_name_plural = 'عناوين الشحن'


class CardInfo(models.Model):
    cc_number = CardNumberField(_('card number'))
    cc_expiry = CardExpiryField(_('expiration date'))
    cc_code = SecurityCodeField(_('security code'))

    class Meta:
        verbose_name = 'معلومات البطاقة'
        verbose_name_plural = 'معلومات البطاقات'


class PaymentMethod(models.Model):
    PAYMETMETHOD = [
        ("الدفع عن الإستلام", "الدفع عن الإستلام"),
        ("بريدي موب", "بريدي موب"),
    ]

    user = models.ForeignKey(
        "users.User", verbose_name="user", on_delete=models.CASCADE, blank=True)
    payment_methods = models.CharField(max_length=20,
                                       choices=PAYMETMETHOD, verbose_name="Payment Methods")
    card_info = models.ForeignKey(
        CardInfo, verbose_name="معلومات البطاقة", on_delete=models.CASCADE, default=1)
    payment_method_date_add = models.DateTimeField(
        auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'طريقة الدفع'
        verbose_name_plural = 'طرق الدفع'


class CodePromo(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.PositiveIntegerField(default=50,
                                                      validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="Discount Percentage")
    is_valide = models.BooleanField(
        verbose_name="is valide", default=False)
    code_date_add = models.DateTimeField(
        auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'كود التخفيض'
        verbose_name_plural = 'كودات التخفيض'


class Order(models.Model):
    customer = models.CharField(verbose_name="customer Name",max_length=50)
    stats = models.ForeignKey(
        State, verbose_name="state delivery", on_delete=models.CASCADE,null=True, blank=True)
    phone_number = models.CharField(
        verbose_name="Phone Number", max_length=10)
    address_complete = models.CharField(
        verbose_name="Address delivery", max_length=150)
    postal_code = models.CharField(
        verbose_name="Postal Code", max_length=10)
    city = models.CharField(
        verbose_name="city delivery", max_length=100, blank=True)

    order_date = models.DateTimeField(verbose_name="Order Date",auto_now_add=True)
    status = models.CharField(verbose_name="Order Status",max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Processed', 'Processed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ], default='Pending')
    payment_status = models.CharField(verbose_name="Payment Status",max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    ], default='Pending')
    order_fk = models.CharField(verbose_name="Chargily Id",max_length=50,blank=False)
    total_price = models.PositiveIntegerField()
    class Meta:
        verbose_name = 'الطلب'
        verbose_name_plural = 'الطلبات'


    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='order',null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE,null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'كتب الطلبات'
        verbose_name_plural = 'كتب الطلبات'


    def __str__(self):
        return self.order.customer
