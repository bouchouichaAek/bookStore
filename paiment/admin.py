from django.contrib import admin
from .models import *

# Register your models here.


class StateAdmin(admin.ModelAdmin):
    list_display = ["state_name", "delivery_price"]


class AddresShipingAdmin(admin.ModelAdmin):
    list_display = ["user", "stats",
                    "address_complete", "postal_code", "phone_number"]


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ["user", "payment_methods"]


class CodePromoAdmin(admin.ModelAdmin):
    list_display = ["code", "discount_percentage", "is_valide"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer","stats","phone_number","address_complete", "postal_code", "city","status", "payment_status","order_fk"]
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "total_price"]


admin.site.register(State, StateAdmin)
admin.site.register(AddresShiping, AddresShipingAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(CodePromo, CodePromoAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
