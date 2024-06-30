from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', blogger, name="blogger"),
    path('<str:articaltitle>', singleArtical, name="single-artical"),
]
