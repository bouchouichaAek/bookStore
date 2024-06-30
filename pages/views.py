from django.shortcuts import render,redirect
from books.models import *
from blogger.models import *
from django.conf import settings
from users.models import *

# Create your views here.


def home(request):

    last_release = Book.objects.filter(
        is_published=True).order_by('-Book_date_add')
    last_release_images = Book.objects.filter(
        is_published=True).order_by('-Book_date_add')[:5]
    soon_release = Book.objects.filter(
        is_accpted=True, is_published=False).order_by('-Book_date_add')
    articals = Artical.objects.filter(
        artical_status="نشر").all().order_by('-artical_date_add')[:3]


    context = {
        "last_release": last_release,
        "soon_release": soon_release,
        "articals": articals,
        "imgs": last_release_images,
    }

    return render(request, 'home-page.html', context)


def Subscriber_register(request):
    if request.method == 'POST':
        # Create a new subscriber
        subscriber_email = request.POST.get('subscriber_email')
        subscriber = Subscriptions(
            subscriber_email=subscriber_email
        )
        subscriber.save()
    return redirect("home")


def ContactUs(request):
    context = {
        "title": "تواصل معنا",
    }

    return render(request, 'contact-us-page.html', context)


def user_agreement(request):
    context = {
        "title": "اتفاقية المستخدم",
    }

    return render(request, 'links/user-agreement.html', context)
