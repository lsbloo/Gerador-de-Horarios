from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(label='Seu Username', max_length=100)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(label='password', max_length=100)
    password2 = forms.CharField(label='confirmation-password', max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label='password', max_length=100)