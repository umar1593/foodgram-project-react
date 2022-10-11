from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = forms.CharField(widget=forms.PasswordInput)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "password"]

    def __str__(self):
        return self.username

    def get_username(self):
        return f"Пользователь {self.email}"
