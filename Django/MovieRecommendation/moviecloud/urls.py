from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('detail/<int:pk>', views.detail),
]