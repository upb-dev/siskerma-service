from django.shortcuts import render
from django.conf import settings

# Create your views here.


def index(request):
    data = {
        "version": settings.VERSION
    }
    return render(request, 'index.html', data)
