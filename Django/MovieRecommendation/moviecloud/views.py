from django.shortcuts import render
from .models import MoiveData
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'moviecloud/home.html')