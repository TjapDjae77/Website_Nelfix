from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import UserRegisterView, UserLoginView, UserProfileView

app_name = 'user'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='film:home'), name='logout'),
]
