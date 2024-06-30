from django import forms
from books.models import *
from users.models import *
from blogger.models import *
from paiment.models import *

from django.utils.translation import gettext_lazy as _


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ("Book_add_by",)

        labels = {
            "book_title": "عنوان الكتاب :",
            "book_subtitle": "عنوان الفرعي للكتاب :",
            "book_category": "نوع الكتاب :",
            "book_author": "الكاتب :",
            "Book_translator": "مترجم الكتاب :",
            "book_discription_summary": "ملخص الكتاب :",
            "book_discription": "تعريف بالكتاب :",
            "book_status": "حالة الكتاب :",
            "is_published": "منشور",
            "is_accpted": "مقبول",
            "book_price": "السعر :",
            "book_picture": "صورة الكتاب :",
            "book_index": "فهرس الكتاب :",
            "book_PDF": " الكتاب (PDF):",
            "book_date_published": "تاريخ النشر :",
            "book_year_published": "سنة النشر :",
        }

        widgets = {
            'book_price': forms.NumberInput(attrs={'class': 'text-start'}),
        }


class BookCategoresForm(forms.ModelForm):
    class Meta:
        model = BooksCategory
        fields = "__all__"

        labels = {
            "category_name": "إسم نوع الكتاب :",
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ("password", "last_login", "groups", "user_permissions")
        labels = {
            "is_verified": "تم التحقق منه",
        }
        help_texts = {
            "is_verified": "يحدد ما إذا كان المستخدم قد أكد بريده الإلكتروني",
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'text-start'}),
        }


class ArticalForm(forms.ModelForm):
    class Meta:
        model = Artical
        exclude = ("artical_date_add", "artical_title",
                   "artical_author", "artical_category", "artical_body", "artical_picture", "artical_picture_body")
        labels = {
            "artical_status": "حالة المقال",
            "reason_of_reject": "سبب رفض المقال ",
        }


class StatesForm(forms.ModelForm):
    class Meta:
        model = State
        fields = "__all__"

        labels = {
            "state_name": "إسم الولاية",
            "delivery_price": "ثمن الشحن للولاية",
        }

        widgets = {
            'delivery_price': forms.NumberInput(attrs={'class': 'text-start'}),
        }


class CodePromoForm(forms.ModelForm):
    class Meta:
        model = CodePromo
        fields = "__all__"

        labels = {
            "code": "الكود",
            "discount_percentage": "نسبة التخفيض",
            "is_valide": "مفعل",
        }

        widgets = {
            'discount_percentage': forms.NumberInput(attrs={'class': 'text-start'}),
        }
