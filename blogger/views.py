from django.shortcuts import render, get_object_or_404, redirect
from .models import *
# Create your views here.


def blogger(request):

    articals = Artical.objects.filter(
        artical_status="نشر").all().order_by('-artical_date_add')

    context = {
        "articals": articals,
        "title": "مدونة القبس",
    }

    return render(request, 'blogger-page.html', context)


def singleArtical(request, articaltitle):

    articaltitle = " ".join(articaltitle.split("-"))
    artical = get_object_or_404(Artical, artical_title=articaltitle)
    outherartical = Artical.objects.exclude(
        artical_title=articaltitle).filter(artical_status="نشر").all()
    print(artical.artical_author)
    if not artical.artical_status == "نشر" and artical.artical_author != request.user and not request.user.is_superuser:
        return redirect("/")

    context = {
        "artical": artical,
        "outherartical": outherartical,
        "title": artical,
    }

    return render(request, 'single-artical-page.html', context)
