import django_filters
from .models import *


class BookFilter(django_filters.FilterSet):

    AUTHORCHOICES = [(i.book_author, i.book_author)
                     for i in Book.objects.all()]

    book_author = django_filters.ChoiceFilter(
        choices=AUTHORCHOICES)

    class Meta:
        model = Book
        fields = ["book_category", "book_author", "book_year_published"]
