from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.username
