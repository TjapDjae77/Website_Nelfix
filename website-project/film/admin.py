from django.contrib import admin

# Register your models here.
from .models import Film

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'release_year', 'genre', 'price', 'duration')
    search_fields = ('title', 'director', 'release_year', 'genre')
    list_filter = ('release_year', 'genre')