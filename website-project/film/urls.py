from . import views
from .views import FilmListCreateView, FilmViewSet, FilmListView, FilmDetailView, FilmAPIDetailView, buy_film
from django.urls import path, include
from rest_framework.routers import DefaultRouter


app_name = 'film'

router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='film')

urlpatterns = [
    # path('ajax/search/', FilmAjaxSearchView.as_view(), name='ajax_search'),
    path('', FilmListView.as_view(), name='home'),
    path('search/', views.film_search, name='film_search'),
    path('films/<int:pk>/', FilmDetailView.as_view(), name='film_detail'),
    path('films/<int:pk>/buy/', buy_film, name='buy_film'),
    path('my-list/', views.my_list, name='my_list'),
]