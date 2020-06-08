from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': "input"}))
    last_name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': "input"}))
    phone = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': "input", "type": 'tel'}))
    address = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': "input"}))
    email = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': "input", 'type': 'email'}))
    password1 = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': "input", 'type': 'password'}))
    password2 = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': "input", 'type': 'password'}))

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'phone', 'address', 'email', 'password1', 'password2')
