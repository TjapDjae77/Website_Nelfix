# from django.contrib import messages
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.views import LoginView, LogoutView
# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.generic import CreateView, DetailView
# from .forms import UserRegisterForm, UserLoginForm
# from .models import Profile

# # Create your views here.


# class UserRegisterView(CreateView):
#     form_class = UserRegisterForm
#     template_name = 'user/register.html'
#     success_url = reverse_lazy('user:login')
    
#     def form_valid(self, form):
#         user = form.save()
#         Profile.objects.create(user=user)
#         login(self.request, user)
#         return redirect(self.success_url)

# class UserLoginView(LoginView):
#     form_class = UserLoginForm
#     template_name = 'user/login.html'

#     def form_valid(self, form):
#         user = form.get_user()
#         if user is not None and user.check_password(form.cleaned_data['password']):
#             login(self.request, user)
#             return redirect('film:home')  # Redirect ke halaman profil setelah login berhasil
#         return super().form_invalid(form)
    
#     def form_invalid(self, form):
#         # Menambahkan pesan kesalahan jika autentikasi gagal
#         print("Username atau password salah.")
#         messages.error(self.request, "Username atau password salah.")
#         return self.render_to_response(self.get_context_data(form=form))

# @method_decorator(login_required, name='dispatch')
# class UserProfileView(LoginRequiredMixin, DetailView):
#     model = Profile
#     template_name = 'user/profile.html'
#     context_object_name = 'profile'

#     def get_object(self):
#         try:
#             profile = Profile.objects.get(user=self.request.user)
#         except Profile.DoesNotExist:
#             return redirect('user:login')  # Redirect ke halaman untuk membuat profil jika tidak ada
#         return profile


from .forms import UserRegisterForm, UserLoginForm
from .models import Profile
from .serializers import AdminLoginSerializer, UserSerializer, ProfileSerializer
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'user': {
                'username': user.username,
                'email': user.email,
            }
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Only accessible by admin


class ProfileFactory:
    @staticmethod
    def create_profile(user):
        return Profile.objects.create(user=user)

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')
    
    def form_valid(self, form):
        user = form.save()
        ProfileFactory.create_profile(user)
        login(self.request, user)
        return redirect(self.success_url)
    
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('film:home')  # Redirect ke halaman utama setelah login berhasil
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, self.template_name, {'form': form})

# class LoginView(APIView):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'status': 'success',
#                 'message': 'Login successful',
#                 'data': {
#                     'username': user.username,
#                     'token': str(refresh.access_token),
#                 }
#             }, status=status.HTTP_200_OK)
#         return Response({'status': 'error', 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class LoginAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return JsonResponse({
#                 'status': 'success',
#                 'message': 'Login successful',
#                 'data': {
#                     'username': user.username,
#                     'access_token': str(refresh.access_token),
#                     'refresh_token': str(refresh),
#                 }
#             }, status=200)
#         return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
    
class SelfView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
    
@method_decorator(login_required, name='dispatch')
class UserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('user:login')
        return profile