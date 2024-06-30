from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from blogger.forms import *
from blogger.models import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from .functions import resize_and_crop_image

# Create your views here.


def registrations(request):
    createuserform = CreateNewUser()
    if request.method == "POST":
        createuserform = CreateNewUser(request.POST)
        if createuserform.is_valid():
            email = request.POST.get("email")

            html = render_to_string("emails/email-confirmation.html")
            send_mail('تأكيد البريد الإلكتروني', "", "bouchouichaaek97@gmail.com",
                      [email], html_message=html)
            createuserform.save()

            username = request.POST.get("username")
            password = request.POST.get("password1")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('verification')
            messages.success(
                request, " Votre compte a été créé avec succès, vous pouvez vous connecter maintenant ")
        else:
            print(createuserform.errors)
            messages.error(
                request, createuserform.errors)
            # print(createuserform)
    context = {
        "form": createuserform,
    }
    return render(request, "authentication/registration.html", context)


@login_required(login_url='login')
def mail_verification(request):
    current_site = get_current_site(request)
    if request.method == "POST":
        html = render_to_string("emails/email-confirmation.html", {
            "username": request.user.username,
            'domain': current_site.domain,
        })
        send_mail('contact me', "Confirm Your Email Address", "bouchouichaaek97@gmail.com",
                  [request.user.email], html_message=html)
    context = {

    }
    return render(request, 'authentication/mail-verification.html', context)


@login_required(login_url='login')
def getVerified(request):

    user = get_object_or_404(User, username=request.user)
    print()
    if request.method == "POST":
        user.is_verified = True
        user.save()
        return redirect('verification')
    context = {

    }
    return render(request, 'authentication/get-email-verified.html', context)


def userlogin(request):

    loginform = LoginForm()
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user_is_active = User.objects.get(email=email)
            user = authenticate(
                request, username=email, password=password)
            if user_is_active.is_active:
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(
                        request, "البريد الإلكتروني او كلمة السر خاطئة")

            else:
                messages.error(
                    request, "حسابك معطل , يبدوا أنك قد خالفت إحدى سياسات المستخدم , إذا تعتقد انه حدث خطأ ما فيمكنك التواصل مع إدارة الموقع عبر الإيمايل التالي : support@alqapas-publishing.com")

        except User.DoesNotExist:
            messages.error(
                request, "لا يوجد مستخدم مسجل بهذا الإيمايل")

    context = {
        "form": loginform
    }
    return render(request, 'authentication/login.html', context)


def forgotPassword(request):

    form = EnterEmail(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        current_site = get_current_site(request)
        mail_subject = 'Reset your password'
        html = render_to_string('emails/reset-password-email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        })
        send_mail(mail_subject, "", 'admin@example.com',
                  [email], html_message=html)
        # Replace with your success page
        return redirect('password_reset_done')
    else:
        form = EnterEmail()

    context = {
        "form": form
    }

    return render(request, 'authentication/forgot-password.html', context)


def password_reset_done(request):
    context = {
        "title": "أرسل البريد الإلكتروني",
    }
    return render(request, 'authentication/password-reset-done.html', context)


def password_reset_confirm(request, uid, token):

    try:
        uid = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                # Replace with your success page
                return redirect('password-reset-complete')
        else:
            form = SetPasswordForm(user)
        context = {
            "title": "إعادة تعيين كلمة المرور",
            "form": form

        }
        return render(request, 'authentication/set-password.html', context)
    else:
        return redirect('password-reset-failed')


def password_reset_complete(request):
    context = {
        "title": "تم تعيين كلمة السر الجديد",
    }
    return render(request, 'authentication/password-reset-complete.html', context)


def password_reset_link_invalid(request):
    context = {
        "title": "الرابط غير صالح",
    }
    return render(request, 'authentication/password-reset-invalidlink.html', context)


@login_required(login_url='login')
def my_profile(request):
    user = User.objects.get(email=request.user.email)
    form = UserChangeForm(instance=user)
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=user)
        print(form.errors)
        for error in form.errors:
            print(error)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "لقد تم تحديث حسابك بنجاح", extra_tags="success")

            return redirect('my-profile')
        else:
            messages.add_message(request, messages.ERROR,
                                 form.errors, extra_tags="errBirthday")

    context = {
        "title": "حسابي",
        "form": form,
    }

    return render(request, 'account/my-profile.html', context)


def add_picture_profile(request):
    user = get_object_or_404(User, username=request.user)
    if 'picture_profile' in request.FILES:
        picture = request.FILES["picture_profile"]
        user.picture = picture
        user.save()
    else:
        pass

    return redirect('my-profile')


@login_required(login_url='login')
def user_change_password(request):
    user = User.objects.get(email=request.user.email)
    form = PasswordChangeForm(user)
    if request.method == "POST":
        form = PasswordChangeForm(user, request.POST)
        print(form.errors)
        for error in form.errors:
            print(error)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "لقد تم تغيير كلمة المرور بنجاح", extra_tags="PassChangeSuccess")
            return redirect('my-profile')
        else:
            messages.add_message(request, messages.WARNING,
                                 form.errors, extra_tags="errPassword")

    context = {
        "title": "تغيير كلمة المرور",
        "form": form,
    }

    return render(request, 'account/change-password.html', context)


@login_required(login_url='login')
def my_articals(request):

    published_articals = Artical.objects.filter(
        artical_author_id=request.user.id, artical_status="نشر")
    not_published_articals = Artical.objects.filter(Q(artical_author_id=request.user.id) &
                                                    (Q(artical_status="قيد الانتظار") | Q(artical_status="مرفوض")))

    context = {
        "title": "مقالاتي",
        "published_articals": published_articals,
        "not_published_articals": not_published_articals,
    }
    return render(request, 'account/my-articals.html', context)


@login_required(login_url='login')
def write_article(request):

    if request.method == "POST":
        form = AricalForm(request.POST, request.FILES)

        print(form)
        messages.add_message(request, messages.WARNING,
                             form.errors, extra_tags="AddArticalfailed")
        if form.is_valid():
            # Don't save yet, we need to set the author
            article = form.save(commit=False)
            article.artical_author = request.user
            article.save()

            messages.add_message(request, messages.SUCCESS,
                                 "لقد تم إضافة المقال بنجاح", extra_tags="AddArticalSeccesfully")
            return redirect('my-articals')
        else:
            messages.add_message(request, messages.WARNING,
                                 form.errors, extra_tags="AddArticalfailed")
    else:
        form = AricalForm()

    context = {
        "title": "أكتب مقالا",
        "form": form,

    }
    return render(request, 'account/write-articale.html', context)


@login_required(login_url='login')
def edit_article(request, artical_title):
    articaltitle = " ".join(artical_title.split("-"))
    artical = get_object_or_404(Artical, artical_title=articaltitle)
    form = AricalForm(instance=artical)
    if request.method == "POST":
        form = AricalForm(request.POST, request.FILES, instance=artical)
        messages.add_message(request, messages.WARNING,
                             form.errors, extra_tags="AddArticalfailed")
        if form.is_valid():
            # Don't save yet, we need to set the author
            article = form.save(commit=False)
            article.artical_author = request.user
            article.save()

            messages.add_message(request, messages.SUCCESS,
                                 "لقد تم تغيير المقال بنجاح", extra_tags="AddArticalSeccesfully")
            return redirect('my-articals')
        else:
            messages.add_message(request, messages.WARNING,
                                 form.errors, extra_tags="AddArticalfailed")
    else:
        form = AricalForm(instance=artical)

    context = {
        "title": "عدّل مقال",
        "artical": artical,
        "form": form,

    }
    return render(request, 'account/edit-object.html', context)


@login_required(login_url='login')
def add_to_favorites(request, item_id):
    # Replace with your item retrieval logic
    item = Book.objects.get(id=item_id)
    Favorite.objects.get_or_create(user=request.user, item=item)
    return redirect('our-books')  # Redirect to favorites page


@login_required(login_url='login')
def remove_from_favorites(request, item_id):
    item = Book.objects.get(id=item_id)
    Favorite.objects.filter(user=request.user, item=item).delete()
    return redirect('our-books')  # Redirect to favorites page


def my_favorites(request):
    books = Favorite.objects.filter(
        user=request.user).order_by("-added_date").all()
    context = {
        "title": "مفضلتي",
        "books": books,

    }
    return render(request, 'account/my-favorites.html', context)


@login_required(login_url='login')
def userlogout(request):
    logout(request)
    return redirect('login')
