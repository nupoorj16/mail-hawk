from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#signup form for taking user's credentials
class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
