from django import forms
from django.contrib.auth.forms import AuthenticationForm

from user.models import User

class UserLoginForm(AuthenticationForm):
    # username = forms.CharField(label='User Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    # password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')