from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150)  # First name
    last_name = models.CharField(max_length=150)  # Last name
    birth_date = models.DateField(null=True, blank=True)  # Birthdate
    email = models.EmailField(unique=True)  # Unique email
    username = models.CharField(max_length=150, unique=True)  # Username field (unique)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profile picture

    # You can also add any additional custom methods or fields here if needed.

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
