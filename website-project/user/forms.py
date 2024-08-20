# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import Profile

# class UserRegisterForm(UserCreationForm):
#     username = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
#             'placeholder': 'Enter your username',
#         })
#     )
#     email = forms.EmailField(
#         required=True,
#         widget=forms.EmailInput(attrs={
#             'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
#             'placeholder': 'Enter your email',
#         })
#     )
#     password1 = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(attrs={
#             'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
#             'placeholder': 'Enter your password',
#         })
#     )
#     password2 = forms.CharField(
#         label="Password confirmation",
#         widget=forms.PasswordInput(attrs={
#             'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
#             'placeholder': 'Confirm your password',
#         })
#     )
#     bio = forms.CharField(
#         widget=forms.Textarea(attrs={
#             'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
#             'placeholder': 'Enter your bio',
#             'rows': 4,
#         }),
#         required=False
#     )

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2', 'bio']

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('Email already registered. Please use a different email.')
#         return email
        

# class UserLoginForm(AuthenticationForm):
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600',
#             'placeholder': 'Enter your username',
#         })
#     )
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={
#             'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600',
#             'placeholder': 'Enter your password',
#         })
#     )


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
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
            'placeholder': 'Enter your first name',
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-transparent',
            'placeholder': 'Enter your last name',
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

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered. Please use a different email.')
        return email

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600',
            'placeholder': 'Enter your email or username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 p-2 w-full rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:border-indigo-600',
            'placeholder': 'Enter your password',
        })
    )

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        # Cek apakah input adalah email
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                username_or_email = user.username  # Ganti input dengan username yang sesuai
            except User.DoesNotExist:
                raise forms.ValidationError("User with this email does not exist.")
        
        # Gunakan input yang sudah disesuaikan untuk autentikasi
        self.cleaned_data['username'] = username_or_email
        return super(UserLoginForm, self).clean()