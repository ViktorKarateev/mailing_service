from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Аватар')
    country = CountryField(blank=True, verbose_name='Страна')  # ✅ новое поле

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
