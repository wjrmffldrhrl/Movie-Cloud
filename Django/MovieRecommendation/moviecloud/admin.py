from django.contrib import admin
from .models import MoiveData

# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director')

admin.site.register(MoiveData, MovieAdmin)