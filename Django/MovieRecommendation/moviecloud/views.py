from django.shortcuts import render
from .models import MovieData
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'moviecloud/home.html')