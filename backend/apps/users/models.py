import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    rating = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255, blank=True)
