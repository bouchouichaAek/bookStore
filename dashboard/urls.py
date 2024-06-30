from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard_main, name="dashboard-main"),
    path('dashboard-books/', dashboard_books, name="dashboard-books"),
    path('dashboard-books-order-published/', dashboard_books_order_published, name="dashboard-books-order-published"),
    path('dashboard-books/add-book', add_book, name="add-book"),
    path('dashboard-books/add-catgory', add_Category, name="add-catgory"),
    path('dashboard-books/<bookname>', view_Book_PDF, name="view-Book-PDF"),
    path('dashboard-articals/', dashboard_articals, name="dashboard-articals"),
    path('dashboard-users/', dashboard_users, name="dashboard-users"),
    path('dashboard-info/', dashboard_Info, name="dashboard-info"),
    path('dashboard-info/add-state', add_States, name="add-state"),
    path('dashboard-info/add-codepromo', add_Codepromo, name="add-codepromo"),
    path('dashboard-order/', dashboard_order, name="dashboard-order"),
    path('dashboard-order/show-order/<order>/', show_order_from_notification, name="dashboard-order-notification"),
    path('<app>/<model>/<int:id>/show', show_object, name='show-object'),
    path('<app>/<model>/<int:id>/edit', edit_object, name="edit-object"),
    path('<app>/<model>/<int:id>/delete', delete_object, name="delete-object"),
]
