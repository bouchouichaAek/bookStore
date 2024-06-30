from django.contrib import admin
from .models import *

# Register your models here.


class BooksCategoryAdmin(admin.ModelAdmin):
    list_display = ["category_name"]


class BookAdmin(admin.ModelAdmin):
    list_display = ["book_title", "book_subtitle", "book_category", "book_author",
                    "Book_translator", "book_status", "is_published", "is_accpted", "book_price", "book_date_published", "book_year_published"]


admin.site.register(BooksCategory, BooksCategoryAdmin)
admin.site.register(Book, BookAdmin)
