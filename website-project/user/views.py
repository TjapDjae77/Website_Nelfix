from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView
from .forms import UserRegisterForm, UserLoginForm
from .models import Profile

# Create your views here.

# def list(request):
#     posts = Movie.objects.all()

#     context = {
#         'page_title':'All Posts',
#         'posts': posts,
#     }
#     return render(request, 'user/list.html', context)

# def create(request):
#     post_form = PostForm(request.POST or None)

#     if request.method == 'POST':
#         if post_form.is_valid():
#             post_form.save()

#             return redirect('user:list')
        
#     context = {
#         'page_title' : 'Create post',
#         'post_form' : post_form,
#     }

#     return render(request, 'user/create.html', context)

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')
    
    def form_valid(self, form):
        user = form.save()
        bio = form.cleaned_data.get('bio')
        Profile.objects.create(user=user, bio=bio)
        login(self.request, user)
        return redirect(self.success_url)

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user is not None and user.check_password(form.cleaned_data['password']):
            login(self.request, user)
            return redirect('film:home')  # Redirect ke halaman profil setelah login berhasil
        return super().form_invalid(form)
    
    def form_invalid(self, form):
        # Menambahkan pesan kesalahan jika autentikasi gagal
        print("Username atau password salah.")
        messages.error(self.request, "Username atau password salah.")
        return self.render_to_response(self.get_context_data(form=form))

@method_decorator(login_required, name='dispatch')
class UserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'user/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        try:
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('user:login')  # Redirect ke halaman untuk membuat profil jika tidak ada
        return profile