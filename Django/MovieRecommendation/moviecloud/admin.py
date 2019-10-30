from django.contrib import admin
from .models import MovieData

# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'director')

admin.site.register(MovieData, MovieAdmin)