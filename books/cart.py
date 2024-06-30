from decimal import Decimal
from django.conf import settings
from .models import *
from paiment.models import *
from django.core import serializers
import json


class Cart(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        address = self.session.get(settings.ADDRESS_SESSION_ID)
        payment = self.session.get(settings.PAYMENT_SESSION_ID)
        promo = self.session.get(settings.PROMO_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        if not address:
            address = self.session[settings.ADDRESS_SESSION_ID] = {}

        if not payment:
            payment = self.session[settings.PAYMENT_SESSION_ID] = {}

        if not promo:
            promo = self.session[settings.PROMO_SESSION_ID] = {}

        self.cart = cart
        self.address = address
        self.payment = payment
        self.promo = promo

    def __iter__(self):
        for p in self.cart:
            self.cart[str(p)]["book"] = Book.objects.get(pk=p)

        for item in self.cart.values():
            item["total_price"] = item["book"].book_price * \
                item["quantity"]

            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, book_id, quantity=1, update_quantity=False):
        book_id = str(book_id)
        if book_id not in self.cart:
            self.cart[book_id] = {
                "book": Book.objects.get(pk=book_id),
                "quantity": int(quantity),
                "id": book_id,

            }

        if update_quantity:
            self.cart[book_id]["quantity"] += quantity
            if self.cart[book_id]["quantity"] == 0:
                self.remove(book_id)

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session[settings.ADDRESS_SESSION_ID] = self.address
        self.session[settings.PAYMENT_SESSION_ID] = self.payment
        self.session[settings.PROMO_SESSION_ID] = self.promo
        self.session.modified = True

    def remove(self, book_id):
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def get_total_book_price(self):

        for p in self.cart.keys():
            self.cart[str(p)]["book"] = Book.objects.get(pk=p)

        return int(sum(item["book"].book_price * item["quantity"] for item in self.cart.values()))

    def add_address(self, dilevery_address):
        self.address = {
            "stats": dilevery_address.getState(),
            "first_name": dilevery_address.getFirstName(),
            "last_name": dilevery_address.getLastName(),
            "phone_number": dilevery_address.getPhoneNumber(),
            "address_complete": dilevery_address.getAddressComplete(),
            "postal_code": dilevery_address.getPostalCode(),
            "city": dilevery_address.getCity()
        }
        self.save()

    def add_payment(self, payment_method, payment_method_status):
        self.payment = {
            "payment": payment_method,
            "status": payment_method_status,
        }
        self.save()

    def add_promo(self, code):
        self.promo = {
            "code": code,
        }
        self.save()

    def get_total_price(self):
        if self.address and self.promo:
            percentage = 100 - self.promo["code"].discount_percentage
            return int((percentage * (State.objects.get(
                state_name=self.address["stats"]).delivery_price + self.get_total_book_price())) / 100)
        if self.address:
            return int(State.objects.get(state_name=self.address["stats"]).delivery_price + self.get_total_book_price())
        if self.promo:
            percentage = 100 - self.promo["code"].discount_percentage
            return int(percentage * self.get_total_book_price()) / 100

        return self.get_total_book_price()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        # del self.session[settings.ADDRESS_SESSION_ID]
        # del self.session[settings.PAYMENT_SESSION_ID]
        # del self.session[settings.PROMO_SESSION_ID]
        self.session.modified = True
        
    def get_item(self, book_id):
        if str(book_id) in self.cart:
            return self.cart[str(book_id)]
        else:
            return None

    def get_dilevery_address(self):
        return self.address

    def get_payment_method(self):
        return self.payment

    def get_code_promo(self):
        return self.promo
