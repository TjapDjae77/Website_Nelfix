from .models import Film
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['id', 'title', 'description', 'director', 'release_year', 'genre', 'price', 'duration', 'video', 'cover_image', 'created_at', 'updated_at']