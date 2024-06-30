from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from users.models import *

# Create your models here.


class Artical(models.Model):
    ARTICALSTATUS = [
        ("نشر", "نشر"),
        ("قيد الانتظار", "قيد الانتظار"),
        ("مرفوض", "مرفوض"),
    ]
    artical_title = models.CharField(
        max_length=100, verbose_name="Artical Title")
    artical_author = models.ForeignKey(
        User, verbose_name="Artical Author", on_delete=models.PROTECT)
    artical_category = models.CharField(
        max_length=100, verbose_name="Artical Category")
    artical_body = RichTextField(_("Artical Content "))
    artical_picture = models.ImageField(
        upload_to='Artical Picture', verbose_name="Artical Picture", blank=True)
    artical_picture_body = models.ImageField(
        upload_to='Artical Picture Body', verbose_name="Artical Picture Body", blank=True)
    artical_status = models.CharField(max_length=30,
                                      choices=ARTICALSTATUS, default=ARTICALSTATUS[1][1],  verbose_name="Artical Status")
    reason_of_reject = models.TextField(
        verbose_name="Reason Of Reject", blank=True)
    artical_date_add = models.DateTimeField(
        auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = 'مقال'
        verbose_name_plural = 'المقالات'

    def __str__(self):
        return self.artical_title
