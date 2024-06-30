from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('', home, name="home"),
    path('contact/', ContactUs, name="contact-us"),
    path('agreement/', user_agreement, name="user-agreement"),
    path('Subscriber-register',Subscriber_register, name="subscriber-register"),
]
