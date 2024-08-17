from django.shortcuts import render
from django.views.generic import ListView
from .models import Film

# Create your views here.
class HomeView(ListView):
    model = Film
    template_name = 'film/home.html'
    context_object_name = 'films'