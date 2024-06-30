from django import forms
from users.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, UserChangeForm, PasswordChangeForm
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget
from PIL import Image
from django.core.files import File


class CreateNewUser(UserCreationForm):
    email = forms.CharField(
        max_length=100, label="البريد الإلكتروني", error_messages={'unique': u'هناك مستخدم مسجل مسبقاً بهذا إيمايل'})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username",
                  "email"]

    def __init__(self, *args, **kwargs):
        super(CreateNewUser, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.TextInput(
            attrs={'placeholder': _("إسم الأول")})
        self.fields['last_name'].widget = forms.TextInput(
            attrs={'placeholder': _("إسم العائلة")})
        self.fields['username'].widget = forms.TextInput(
            attrs={'placeholder': _("إسم المستخدم")})
        self.fields['email'].widget = forms.TextInput(
            attrs={'placeholder': _("البريد الإلكتروني")})
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': _("كلمة المرور")})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': _("تأكيد كلمة المرور")})


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]
        labels = {
            "password": "كلمة السر"
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(
            attrs={'placeholder': _("البريد الإلكتروني")})
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'placeholder': _("كلمة المرور")})


class EnterEmail(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(EnterEmail, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(
            attrs={'placeholder': _("اكتب إيمايلك هنا")})


class SetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={'placeholder': _("كلمة المرور الجديدة")})
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={'placeholder': _("تأكيد كلمة المرور الجديدة")})


class UserChangeForm(forms.ModelForm):
    GENDER = [
        ("ذكر", "ذكر"),
        ("أنثى", "أنثى"),
    ]
    gender = forms.ChoiceField(
        label="الجنس", required=False, choices=GENDER)
    birthday = forms.DateField(
        required=False, label="تاريخ الميلاد")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username",
                  "email", "gender", "birthday"]

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={'placeholder': _("إسم المستخدم")})
        self.fields['first_name'].widget = forms.TextInput(
            attrs={'placeholder': _("إسم الأول")})
        self.fields['last_name'].widget = forms.TextInput(
            attrs={'placeholder': _("إسم العائلة")})
        self.fields['email'].widget = forms.EmailInput(
            attrs={'placeholder': _("عنوان بريد إلكتروني")})
        self.fields['birthday'].widget = forms.TextInput()


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(
            attrs={'placeholder': _("كلمة المرور القديمة")})
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={'placeholder': _("كلمة المرور الجديدة")})
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={'placeholder': _("تأكيد كلمة المرور الجديدة")})


# class PhotoForm(forms.ModelForm):
#     x = forms.FloatField(widget=forms.HiddenInput())
#     y = forms.FloatField(widget=forms.HiddenInput())
#     width = forms.FloatField(widget=forms.HiddenInput())
#     height = forms.FloatField(widget=forms.HiddenInput())

#     class Meta:
#         model = User
#         fields = ('picture', 'x', 'y', 'width', 'height', )

#     def save(self):
#         photo = super(PhotoForm, self).save()

#         x = self.cleaned_data.get('x')
#         y = self.cleaned_data.get('y')
#         w = self.cleaned_data.get('width')
#         h = self.cleaned_data.get('height')

#         image = Image.open(photo.picture)
#         cropped_image = image.crop((x, y, w+x, h+y))
#         resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
#         resized_image.save(photo.picture.path)

#         return photo
