from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    solo = models.BooleanField(blank=True, null=True)
    hour_price = models.FloatField(blank=True, null=True)
