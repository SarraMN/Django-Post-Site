# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150)  # Prénom
    last_name = models.CharField(max_length=150)  # Nom de famille
    birth_date = models.DateField(null=True, blank=True)  # Date de naissance
    email = models.EmailField(unique=True)  # Email unique
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Numéro de téléphone
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Photo de profil
    address = models.TextField(blank=True, null=True)  # Adresse
    password = models.CharField(max_length=255)  # Mot de passe (géré par Django)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
