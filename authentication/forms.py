# authentication/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField()
    username = forms.CharField(max_length=150)  # Removed the unique argument
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'birth_date', 'email', 'profile_picture', 'password1', 'password2']