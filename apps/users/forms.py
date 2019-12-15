from django import forms
from authtools.forms import UserCreationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text='Required')

    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'password1', 'password2', 'image']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'username', 'image']