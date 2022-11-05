import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# class UserManager(BaseUserManager):
#
#     def create_user(self, email, password=None, **extra_fields):
#         """Creates and saves a new user"""
#         if not email:
#             raise ValueError('User must have an email address')
#         user = self.model(email=self.normalize_email(email), **extra_fields)
#         user.set_password(password)
#         user.save()
#
#         return user
#
#     def create_superuser(self, email, password):
#         """Creates and saves a new super user"""
#         user = self.create_user(email, password)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save()
#
#         return user


class User(AbstractUser):
    """Custom user model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=50)
    rating = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=255)
    # last_activity = models.DateTimeField()

