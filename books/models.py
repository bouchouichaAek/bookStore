from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from users.models import *
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class BooksCategory(models.Model):
    category_name = models.CharField(
        max_length=50, verbose_name="Category Name")

    class Meta:
        verbose_name = 'نوع الكتاب'
        verbose_name_plural = 'نوع الكتب'

    def __str__(self):
        return self.category_name


class Book(models.Model):

    BOOKSTATUS = [
        ("نشر", "نشر"),
        ("قيد الانتظار", "قيد الانتظار"),
        ("مرفوض", "مرفوض"),
    ]
    YEARSCHOICES = [(str(i), str(i))
                    for i in range(1900, datetime.date.today().year)]

    book_title = models.CharField(
        max_length=100, verbose_name="Book Title")
    book_subtitle = models.CharField(
        max_length=100, verbose_name="Book Sub Title", blank=True)
    book_category = models.ForeignKey(
        BooksCategory, verbose_name="Book Category", on_delete=models.CASCADE)
    book_author = models.CharField(
        max_length=100, verbose_name="Book Author")
    Book_translator = models.CharField(
        max_length=100, verbose_name="Book Translator", blank=True)
    book_discription_summary = RichTextField(_("Book Discription Sammry"))
    book_discription = RichTextField(_("Book Discription "))
    book_status = models.CharField(max_length=20,
                                   choices=BOOKSTATUS, default=BOOKSTATUS[1], verbose_name="Book Status")
    is_published = models.BooleanField(
        verbose_name="is published", default=False)
    is_accpted = models.BooleanField(
        verbose_name="is accpted", default=False, blank=True)
    book_price = models.PositiveIntegerField(verbose_name="Book Price")
    book_picture = models.ImageField(
        upload_to='Book product', verbose_name="Book Picture", blank=True)
    book_index = models.FileField(
        upload_to="Book index", verbose_name="Book index", blank=True)
    book_PDF = models.FileField(
        upload_to="Book PDF", verbose_name="Book PDF", null=True, blank=True)
    book_date_published = models.DateField(
        blank=True, null=True, default=False)
    book_year_published = models.CharField(
        max_length=20, choices=YEARSCHOICES, verbose_name="Book Year Published")
    Book_date_add = models.DateTimeField(
        auto_now=False, auto_now_add=True)
    Book_add_by = models.ForeignKey(
        "users.User", verbose_name="Book add by", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'كتاب'
        verbose_name_plural = 'الكتب'

    def __str__(self):
        return self.book_title

    def yearpublished(self):
        return self.book_date_published.strftime('%Y')


class Comments(models.Model):
    book = models.ForeignKey(
        Book, verbose_name=_("Book"), on_delete=models.CASCADE)
    commentator_name = models.CharField(
        max_length=100, verbose_name="Commentator Name")
    commentator_email = models.EmailField(
        max_length=100, verbose_name="Commentator Email")
    commentator_rating = models.PositiveIntegerField(default=1,
                                                     validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Rating")
    comments_body = models.TextField(
        max_length=100, verbose_name="Commentator Rating")

    class Meta:
        verbose_name = 'تعليق'
        verbose_name_plural = 'التعليقات'

    def __str__(self):
        return self.commentator_name
