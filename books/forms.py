from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _


class CommentsForm(forms.ModelForm):
    commentator_name = forms.CharField(
        max_length=100, label="إسمك بالكامل")
    commentator_email = forms.EmailField(
        max_length=100, label="بريدك الإلكتروني")
    comments_body = forms.CharField(
        max_length=1000, label="أكتب تعليقا")

    class Meta:
        model = Comments
        exclude = ("book", "commentator_rating")

    def __init__(self, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)
        self.fields['commentator_name'].widget = forms.TextInput(
            attrs={'placeholder': _("إسمك بالكامل"), })
        self.fields['commentator_email'].widget = forms.EmailInput(
            attrs={'placeholder': _("بريدك الإلكتروني"), "class": "text-start"})
        self.fields['comments_body'].widget = forms.Textarea(
            attrs={'placeholder': _("أكتب تعليقا"), })
