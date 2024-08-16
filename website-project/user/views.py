from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm
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
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        bio = form.cleaned_data.get('bio')
        Profile.objects.create(user=user, bio=bio)
        login(self.request, user)
        return redirect(self.success_url)

class UserLoginView(LoginView):
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('index')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')