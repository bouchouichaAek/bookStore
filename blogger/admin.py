from django.contrib import admin
from .models import *
# Register your models here.


class ArticalAdmin(admin.ModelAdmin):
    pass


admin.site.register(Artical)
