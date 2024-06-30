from django.urls import path
from .views import *

urlpatterns = [
    path('', ourbooks, name="our-books"),
    path('add_to_cart/<book_pk>',
         add_to_cart, name="add_to_cart"),
    path('add_book_to_cart/<book_pk>',
         add_book_to_cart, name="add-book-to-cart"),
    path('remove_from_cart/<book_pk>/',
         remove_from_cart, name="remove-from-cart"),
    path('update_cart/<book_pk>/<action>',
         update_cart, name="update_cart"),
    path('clear_cart/',
         clear_cart, name="clear-cart"),
    path('hx_menu_cart', hx_menu_cart, name="hx_menu_cart"),

    path('<str:bookname>/', SingleBook, name="single-book"),
]
