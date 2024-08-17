from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
            'placeholder': 'Enter your username',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
            'placeholder': 'Enter your email',
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
            'placeholder': 'Enter your password',
        })
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
            'placeholder': 'Confirm your password',
        })
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
            'placeholder': 'Enter your bio',
            'rows': 4,
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered. Please use a different email.')
        return email
        # help_texts = {
        #     'username': None,
        #     'password1': None,
        #     'password2': None,
        # }
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     for fieldname in ['username', 'password1', 'password2']:
        #         self.fields[fieldname].help_text = None

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data.get('email')
    #     if commit:
    #         user.save()
    #         Profile.objects.create(user=user, bio=self.cleaned_data.get('bio'))
    #     return user

class UserLoginForm(AuthenticationForm):
    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={
    #         'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-blue-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600',
    #         'placeholder': 'Enter your username',
    #     })
    # )
    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={
    #         'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600',
    #         'placeholder': 'Enter your password',
    #     })
    # )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600',
            'placeholder': 'Enter your username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600',
            'placeholder': 'Enter your password',
        })
    )