from .views import FilmAPIDetailView, LoginAPIView, FilmAPIListCreateView, UserListAPIView, UserAPIDetailView, UserBalanceUpdateView, UserDeleteView, SelfRetrieveView
from django.urls import path


urlpatterns = [
    path('films/', FilmAPIListCreateView.as_view(), name='api-film-list-create'),
    path('films/<int:pk>/', FilmAPIDetailView.as_view(), name='api-film-detail'),
    path('login/', LoginAPIView.as_view(), name='api-user-login'),
    path('self/', SelfRetrieveView.as_view(), name='api-self-retrieve'),
    path('users/', UserListAPIView.as_view(), name='api-user-list'),
    path('users/<int:pk>/', UserAPIDetailView.as_view(), name='api-user-detail'),
    path('users/<int:pk>/balance/', UserBalanceUpdateView.as_view(), name='api-user-balance-update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='api-user-delete'),
]