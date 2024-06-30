from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .filters import *
from .forms import *
from django.contrib import messages
from .cart import Cart
from django.conf import settings
from django.http import FileResponse
import os

# Create your views here.


def ourbooks(request):
    last_release = Book.objects.filter(
        is_published=True).order_by('-Book_date_add')
    filter = BookFilter(request.GET, last_release)
    last_release = filter.qs
    context = {
        "books": last_release,
        "filter": filter,
        "title": "إصدارتنا",
    }

    return render(request, 'our-books-page.html', context)


def SingleBook(request, bookname):
    book_name = bookname
    bookname = " ".join(bookname.split("-"))

    book = get_object_or_404(Book, book_title=bookname)
    comments = Comments.objects.filter(book=book)

    outherbooks = Book.objects.filter(
        book_category=book.book_category, is_published=True).exclude(book_title=bookname)

    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.book = book
            comment.commentator_rating = request.POST.get("rating")
            comment.save()
            messages.success(
                request, " لقد أضفت التعليق بالنجاح", extra_tags="AddComments")
            return redirect('single-book', book_name)
    else:
        form = CommentsForm()
    context = {
        "book": book,
        "comments": comments,
        "title": book,
        "books": outherbooks,
        "form": form,
    }

    return render(request, 'single-book-page.html', context)


def add_to_cart(request, book_pk):

    cart = Cart(request)
    cart.add(book_pk)

    return render(request, 'base/menu-cart.html')


def remove_from_cart(request, book_pk):

    cart = Cart(request)
    cart.remove(book_pk)

    response = render(request, 'paiment/cart.html')
    response["HX-Trigger"] = "update_menu_cart"
    return response


def update_cart(request, book_pk, action):
    cart = Cart(request)

    if action == "increment":
        cart.add(book_pk, 1, True)
    else:
        cart.add(book_pk, -1, True)

    product = get_object_or_404(Book, pk=book_pk)
    quantity = cart.get_item(book_pk)

    if quantity:
        quantity = quantity["quantity"]
        item = {
            "product": {
                "id": product.id,
                "product_name": product.book_title,
                "product_new_price": product.book_price,
            },
            "total_price": quantity * product.book_price,
            "quantity": quantity,
        }
    else:
        item = None

    response = render(request, 'paiment/cart.html', {"item": item})
    response["HX-Trigger"] = "update_menu_cart"
    return response


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("our-books")


def hx_menu_cart(request):
    return render(request, 'base/menu-cart.html')


def add_book_to_cart(request, book_pk):
    if request.method == "POST":
        quantity = request.POST.get("quntity-number")
        cart = Cart(request)
        cart.add(book_pk, quantity=quantity)
        return redirect("our-books")

    return redirect("our-books")
