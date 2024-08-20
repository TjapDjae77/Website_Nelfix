from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import AdminLoginView, UserViewSet, UserRegisterView, LoginAPIView, UserLoginView, SelfView, UserProfileView
from rest_framework.routers import DefaultRouter

app_name = 'user'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('self', SelfView.as_view(), name='self'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='film:home'), name='logout'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('api/', include(router.urls)),
]
