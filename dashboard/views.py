from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from books.models import *
from publishbooks.models import *
from users.models import *
from paiment.models import *
from blogger.models import *
from .forms import *
from django.apps import apps
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.http import HttpResponse
import os
from paiment.forms import OrderForm
from notifications.models import Notification
# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def dashboard_main(request):

    context = {
        "title": "الرئيسية",
        "book_published_number": Book.objects.filter(is_published=True).count(),
        "book_not_published_number": Book.objects.filter(is_published=False).count(),
        "user_number": User.objects.all().count(),
        "admin_number": User.objects.filter(is_superuser=True).count(),
        "all_books": Book.objects.all(),
        "all_users": User.objects.all(),
        "all_articals": Artical.objects.all(),
    }

    return render(request, 'dashboard/dashboard-main.html', context)


@user_passes_test(lambda u: u.is_superuser)
def dashboard_books(request):

    context = {
        "title": "الكتب",
        "all_books": Book.objects.all(),
        "all_Book_categories": BooksCategory.objects.all(),
    }

    return render(request, 'dashboard/dashboard-books.html', context)


@user_passes_test(lambda u: u.is_superuser)
def dashboard_books_order_published(request):
    context = {
        "title": "الكتب المطلوبة لنشر",
        "all_books": BookPublishedOrder.objects.all(),
    }

    return render(request, 'dashboard/dashboard-books-order-published.html', context)


@user_passes_test(lambda u: u.is_superuser)
def view_Book_PDF(request, bookname):

    book = get_object_or_404(Book, book_title=bookname)

    pdf_file_path = os.path.join(
        settings.BASE_DIR, 'upload', str(book.book_PDF))
    print(pdf_file_path)
    with open(pdf_file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(),
                                content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response


@user_passes_test(lambda u: u.is_superuser)
def dashboard_articals(request):

    context = {
        "title": "مقالات",
        "all_articals": Artical.objects.all(),
    }

    return render(request, 'dashboard/dashboard-articals.html', context)


@user_passes_test(lambda u: u.is_superuser)
def dashboard_users(request):

    context = {
        "title": "المستخدمين",
        "all_users": User.objects.all(),
    }

    return render(request, 'dashboard/dashboard-users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def dashboard_Info(request):

    context = {
        "title": "معلومات الفواتير",
        "all_states": State.objects.all(),
        "all_codes": CodePromo.objects.all(),
    }

    return render(request, 'dashboard/dashboard-info.html', context)


@user_passes_test(lambda u: u.is_superuser)
def dashboard_order(request):

    context = {
        "title": "طلبات الشراء",
        "all_order": Order.objects.all(),
        "all_order_items": OrderItem.objects.all(),
    }

    return render(request, 'dashboard/dashboard-order.html', context)


@user_passes_test(lambda u: u.is_superuser)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            object = form.save(commit=False)
            object.Book_add_by = request.user
            print(form.errors)
            object.save()
            return redirect('dashboard-main')
    else:
        form = BookForm()

    context = {
        "title": "أضق كتابا",
        "form": form,
    }
    return render(request, 'dashboard/create-objects/add-book.html', context)


@user_passes_test(lambda u: u.is_superuser)
def add_Category(request):
    if request.method == 'POST':
        form = BookCategoresForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-books')
    else:
        form = BookCategoresForm()

    context = {
        "title": "أضق نوعا جديد من الكتب",
        "form": form,
    }
    return render(request, 'dashboard/create-objects/add-category.html', context)


@user_passes_test(lambda u: u.is_superuser)
def add_States(request):
    if request.method == 'POST':
        form = StatesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-info')
    else:
        form = StatesForm()

    context = {
        "title": "أضق ولاية جديدة",
        "form": form,
    }
    return render(request, 'dashboard/create-objects/add-category.html', context)


@user_passes_test(lambda u: u.is_superuser)
def add_Codepromo(request):
    if request.method == 'POST':
        form = CodePromoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-info')
    else:
        form = CodePromoForm()

    context = {
        "title": "أضق كود التخفيض",
        "form": form,
    }
    return render(request, 'dashboard/create-objects/add-category.html', context)


@user_passes_test(lambda u: u.is_superuser)
def edit_object(request, app, model, id):
    print(app)
    print(model)
    print(id)

    model_classes = {
        'book': (Book, BookForm),
        'user': (User, UserForm),
        'artical': (Artical, ArticalForm),
        'bookscategory': (BooksCategory, BookCategoresForm),
        'state': (State, StatesForm),
        'codepromo': (CodePromo, CodePromoForm),
        'order': (Order, OrderForm),
        # Add more models as needed
    }

    model_class, model_form = model_classes.get(model.lower())

    # if not model_class:
    #     return redirect('error_page')

    instance = get_object_or_404(model_class, pk=id)

    if request.method == 'POST':
        form = model_form(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            if model_form._meta.model == Artical:
                if request.POST.get("artical_status") == "نشر" or request.POST.get("artical_status") == "مرفوض":
                    html = render_to_string("emails/email-articals-status.html", {
                        "title": str(instance),
                        "link": str(instance).replace(' ', '-'),
                        "status": request.POST.get("artical_status"),
                        "reason_of_rejcted": request.POST.get("reason_of_reject")
                    })
                    send_mail('contact me', "Confirm Your Email Address", "bouchouichaaek97@gmail.com",
                              [instance.artical_author.email], html_message=html)

            return redirect('dashboard-main')
    else:
        form = model_form(instance=instance)

    context = {
        "form": form,
        "title": str(instance) + "| عدل ",
        "instance_title": instance,
        "object_name": model_class._meta.verbose_name.title(),
    }

    return render(request, 'dashboard/edit-object.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_object(request, app, model, id):

    model_classes = {
        'book': (Book, BookForm),
        'user': (User, UserForm),
        'artical': (Artical, ArticalForm),
        'bookscategory': (BooksCategory, BookCategoresForm),
        'state': (State, StatesForm),
        'codepromo': (CodePromo, CodePromoForm),
        'order': (Order, OrderForm),
    }
    model_class, model_form = model_classes.get(model.lower())

    instance = get_object_or_404(model_class, pk=id)

    if request.method == 'POST':
        instance.delete()
        return redirect('dashboard-main')

    context = {
        "title": "هل انت متأكد ؟",
        "instance_title": instance,
        "object_name": model_class._meta.verbose_name.title(),

    }
    return render(request, 'dashboard/delete-object.html', context)


@user_passes_test(lambda u: u.is_superuser)
def show_object(request,app, model, id):
    model_classes = {
        'book': (Book, BookForm),
        'user': (User, UserForm),
        'artical': (Artical, ArticalForm),
        'bookscategory': (BooksCategory, BookCategoresForm),
        'state': (State, StatesForm),
        'codepromo': (CodePromo, CodePromoForm),
        'order': (Order, OrderForm),
    }
    model_class, model_form = model_classes.get(model.lower())
    instance = get_object_or_404(model_class, pk=id)
    context = {
        "title": str(instance) + "| عرض ",
        "instance": instance,
        "object_name": model_class._meta.verbose_name.title(),
    }
    if model== "order":
      notification = Notification.objects.get(order=instance.pk)
      notification.viewed = True
      notification.save()
      template = "dashboard/show-objects/show-order.html"
      order_items = OrderItem.objects.filter(order=instance)
      context["order_items"] = order_items

  
    return render(request,template,context)


def show_order_from_notification(request,order):
    order = get_object_or_404(Order, pk=order)
    notification = Notification.objects.get(order=order.pk)
    notification.viewed = True
    notification.save()
    order_items = OrderItem.objects.filter(order=order)
    context = {
        "order":order,
        "order_items":order_items,
        "title": str(order) + "| عرض ",

    }
    
    return render(request,"dashboard/show-objects/show-order-customized.html",context)