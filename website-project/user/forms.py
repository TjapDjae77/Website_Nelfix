from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'bio']

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data.get('email')
    #     if commit:
    #         user.save()
    #         Profile.objects.create(user=user, bio=self.cleaned_data.get('bio'))
    #     return user