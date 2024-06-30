from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _

# Create your models here.


class BookPublishedOrder(models.Model):
    author_name = models.CharField(
        max_length=100, verbose_name="Author Name")
    author_summary = models.TextField(verbose_name="Author summary")
    book_title = models.CharField(
        max_length=100, verbose_name="Book Title")
    book_subtitle = models.CharField(
        max_length=100, verbose_name="Book Sub Title", blank=True)
    book_category = models.CharField(max_length=100,
                                     verbose_name="Book Category")
    book_summary = models.TextField(verbose_name="Book summary")

    book_picture = models.ImageField(
        upload_to='Book Published Order', verbose_name="Book Picture")
    email_address = models.CharField(
        max_length=100, verbose_name="Email Address")
    phone_number = models.CharField(
        max_length=100, verbose_name="Phone Number")
    facebook_account = models.CharField(
        _("Facebook Account"), max_length=200)
    instgram_account = models.CharField(
        _("Instgram Account"), max_length=200)
    twitter_account = models.CharField(
        _("Twitter Account"), max_length=200)
    book_PDF = models.FileField(
        upload_to="Book PDF", verbose_name="Book PDF")

    class Meta:
        verbose_name = 'كتاب مطلوب للنشر'
        verbose_name_plural = 'الكتب المطلوبة للنشر'

    def __str__(self):
        return self.author_name
