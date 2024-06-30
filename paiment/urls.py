from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('cart/', cart, name="cart"),
    path('checkout/', checkout, name="checkout"),
    path('checkout/add-method-payment',
         add_method_payment, name="add-method-payment"),
    path('checkout/add-code-promo',
         add_code_promo, name="add-code-promo"),
    path('create-payment/', create_payment, name='create_payment'),
    path('payment-webhook/', payment_webhook, name='payment_webhook'),
]
