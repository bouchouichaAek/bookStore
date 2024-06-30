from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
from django.forms import ModelForm


class AddresSipingForm(forms.ModelForm):
    class Meta:
        model = AddresShiping
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        super(AddresSipingForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget = forms.TextInput(
            attrs={'placeholder': _("رقم الهاتف"), })
        self.fields['address_complete'].widget = forms.TextInput(
            attrs={'placeholder': _("العنوان الكامل")})
        self.fields['postal_code'].widget = forms.TextInput(
            attrs={'placeholder': _("الرقم البريدي"), })
        self.fields['city'].widget = forms.TextInput(
            attrs={'placeholder': _("المدينة"), })


class CardInfoForm(forms.ModelForm):
    class Meta:
        model = CardInfo
        fields = ("cc_number", "cc_expiry", "cc_code")

    def __init__(self, *args, **kwargs):
        super(CardInfoForm, self).__init__(*args, **kwargs)
        self.fields['cc_number'].widget = forms.TextInput(
            attrs={'placeholder': _("رقم البطاقة"), })
        self.fields['cc_code'].widget = forms.TextInput(
            attrs={'placeholder': _("رمز أمان")})


class OrderForm(forms.ModelForm):
     class Meta:
        model = Order
        fields = '__all__'