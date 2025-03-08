from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'Usuário'),
        ('provider', 'Prestador'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
