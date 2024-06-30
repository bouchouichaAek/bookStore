from django import forms
from .models import *
from users.models import *
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget


class AricalForm(forms.ModelForm):
    artical_title = forms.CharField(
        max_length=100, label="عموان المقال")
    artical_category = forms.CharField(
        max_length=100, label="نوع المقال")
    artical_body = forms.CharField(
        widget=CKEditorWidget(), label="محتوى المقال")

    class Meta:
        model = Artical
        exclude = ("artical_author", "artical_status", "reason_of_reject")
        labels = {
            'artical_picture': 'الصورة الرئيسية للمقال',
            'artical_picture_body': 'الصورة محتوى المقال',
        }
        widgets = {
            'artical_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'artical_picture_body': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', "")
        super(AricalForm, self).__init__(*args, **kwargs)
        self.fields['artical_title'].widget = forms.TextInput(
            attrs={'placeholder': _("عنوان المقال")})
        self.fields['artical_category'].widget = forms.TextInput(
            attrs={'placeholder': _("نوع المقال")})
