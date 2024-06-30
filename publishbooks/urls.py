from django.urls import path, include
from .views import *

urlpatterns = [
    path('', publishbook, name="publish-book"),
]
