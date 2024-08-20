from .models import Film
from .serializers import FilmSerializer
from .strategies import TitleOrDirectorFilterStrategy, AllFilmsStrategy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.decorators.http import require_GET
from django.views.generic import ListView, DetailView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from typing import Any
from user.models import Profile


# Create your views here.

class FilmListCreateView(ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Film created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            films = Film.objects.filter(title__icontains=query) | Film.objects.filter(director__icontains=query)
        else:
            films = self.get_queryset()
        serializer = self.get_serializer(films, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAdminUser]  # Only accessible by admin

    def perform_destroy(self, instance):
        # Delete associated media files when a film is deleted
        if instance.cover_image_url:
            instance.cover_image_url.delete(save=False)
        if instance.video_url:
            instance.video_url.delete(save=False)
        super().perform_destroy(instance)



class FilmListView(ListView):
    model = Film
    template_name = 'film/home.html'
    context_object_name = 'films'
    paginate_by = 4

    def get_query(self):
        return self.request.GET.get('q')
    
    def filter_queryset(self, query):
        if query:
            return TitleOrDirectorFilterStrategy()
        return AllFilmsStrategy()
    
    def get_queryset(self):
        query = self.get_query()
        filtered_queryset = self.filter_queryset(query)
        return filtered_queryset.filter(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.get_query()
        if query:
            context['query'] = query
        return context

    def get_pagination_url(self, page_number):
        query = self.get_query()
        base_url = reverse('film:home')
        params = {'page': page_number}
        if query:
            params['q'] = query
        return f"{base_url}?{urlencode(params)}"

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        paginator, page, queryset, is_paginated = self.paginate_queryset(self.object_list, self.paginate_by)
        context['page_obj'] = page
        context['paginator'] = paginator
        context['is_paginated'] = is_paginated
        context['pagination_url'] = self.get_pagination_url
        return self.render_to_response(context)




class FilmDetailView(DetailView):
    model = Film
    template_name = 'film/film_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)
            context['profile'] = profile
            context['has_bought'] = film in profile.films.all()
        else:
            context['has_bought'] = False

        return context


class FilmAPIDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        film = self.get_object()
        serializer = self.get_serializer(film)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        film = self.get_object()
        serializer = self.get_serializer(film, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "message": "Film updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        film = self.get_object()
        film.delete()
        return Response({"status": "success", "message": "Film deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@login_required
def buy_film(request, pk):
    film = get_object_or_404(Film, pk=pk)
    profile = get_object_or_404(Profile, user=request.user)

    if profile.balance >= film.price:
        profile.balance -= film.price
        profile.films.add(film)
        profile.save()
        messages.success(request, 'You have successfully purchased the film.')
    else:
        messages.error(request, 'Insufficient balance to buy this film.')

    return redirect('film:film_detail', pk=pk)

@login_required
def my_list(request):
    user_profile = request.user.profile
    films = user_profile.films.all()
    return render(request, 'film/my_list.html', {'films': films})

@require_GET
def film_search(request):
    query = request.GET.get('q', '')
    films = Film.objects.filter(title__icontains=query) | Film.objects.filter(director__icontains=query)
    films_data = [
        {
            "title": film.title,
            "release_year": film.release_year,
            "description": film.description[:100] + "...",
            "cover_image_url": film.cover_image_url,
        }
        for film in films
    ]
    return JsonResponse({'films': films_data})