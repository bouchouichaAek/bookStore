from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .models import *

# Create your views here.


def publishbook(request):

    if request.method == "POST":
        formBookPublishedOrder = BookPublishedOrderForm(
            request.POST, request.FILES)
        if formBookPublishedOrder.is_valid():
            book = formBookPublishedOrder.save(commit=False)
            book.book_PDF = "Book PDF/" + request.POST.get("book_PDF")
            book.book_picture = "Book Published Order/" + \
                request.POST.get("image")
            book.save()
            messages.success(
                request, "لقد أدخلت معلومات مؤلفك بنجاح , ستتلقى رسالة قريبا")
            return redirect("publish-book")
        else:

            messages.error(
                request, " هناك خطأ لم تتمكن من إدخال مؤلفك , يرجى اعادة المحاولة")
            return redirect("publish-book")
    else:
        formBookPublishedOrder = BookPublishedOrderForm()
    context = {
        "title": "أنشر كتابك",
        "form": formBookPublishedOrder,
    }

    return render(request, 'publish-book-page.html', context)
