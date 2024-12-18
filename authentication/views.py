# authentication/views.py
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

# Vue d'inscription
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('authentication:login')  # Rediriger vers la page de connexion
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/signup.html', {'form': form})

# Vue de connexion
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('blog:post_list')  # Rediriger vers la liste des publications après la connexion
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

# Vue de déconnexion
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('blog:post_list')  # Rediriger vers la liste des publications après la déconnexion
