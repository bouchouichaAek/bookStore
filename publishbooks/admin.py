from django.contrib import admin
from .models import *
# Register your models here.


class BookPublishedOrderAdmin(admin.ModelAdmin):
    pass


admin.site.register(BookPublishedOrder, BookPublishedOrderAdmin)
