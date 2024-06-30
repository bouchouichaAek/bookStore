from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _


class BookPublishedOrderForm(forms.ModelForm):
    author_name = forms.CharField(
        max_length=100, label="إسم الكاتب")
    author_summary = forms.CharField(label="ملخص عن الكاتب")
    book_title = forms.CharField(
        max_length=100, label="عنوان الكتاب")
    book_subtitle = forms.CharField(
        max_length=100, label="عنوان الفرعي للكتاب", required=False)
    book_category = forms.CharField(
        max_length=100, label="نوع الكتاب", help_text="100 characters max.", required=False)
    book_summary = forms.CharField(label="ملخص عن الكتاب")
    email_address = forms.EmailField(
        max_length=300, label="البريد الإلكتروني")
    phone_number = forms.CharField(
        max_length=300, label="رقم التواصل")
    facebook_account = forms.CharField(
        max_length=300, label="حساب الفيسبوك", required=False)
    instgram_account = forms.CharField(
        max_length=300, label="حساب انستغرام", required=False)
    twitter_account = forms.CharField(
        max_length=300, label="حساب تويتر", required=False)

    class Meta:
        model = BookPublishedOrder
        exclude = ("book_PDF", "book_picture")

    def __init__(self, *args, **kwargs):
        super(BookPublishedOrderForm, self).__init__(*args, **kwargs)
        self.fields['author_name'].widget = forms.TextInput(
            attrs={'placeholder': _("إسم الكاتب"), })
        self.fields['book_title'].widget = forms.TextInput(
            attrs={'placeholder': _("عنوان الكتاب"), })
        self.fields['book_subtitle'].widget = forms.TextInput(
            attrs={'placeholder': _("عنوان الفرعي للكتاب"), })
        self.fields['book_category'].widget = forms.TextInput(
            attrs={'placeholder': _("نوع الكتاب"), })
        self.fields['book_summary'].widget = forms.Textarea(
            attrs={'placeholder': _("ملخص عن الكتاب"), })
        self.fields['author_summary'].widget = forms.Textarea(
            attrs={'placeholder': _("ملخص الكاتب"), })
        self.fields['email_address'].widget = forms.TextInput(
            attrs={'placeholder': _("البريد الإلكتروني"), })
        self.fields['phone_number'].widget = forms.TextInput(
            attrs={'placeholder': _("رقم التواصل"), })
        self.fields['facebook_account'].widget = forms.TextInput(
            attrs={'placeholder': _("حساب الفيسبوك"), "class": "text-start"})
        self.fields['instgram_account'].widget = forms.TextInput(
            attrs={'placeholder': _("حساب انستغرام"), "class": "text-start"})
        self.fields['twitter_account'].widget = forms.TextInput(
            attrs={'placeholder': _("حساب تويتر"), "class": "text-start"})
