from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,username, email, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email")

        user = self.model(username=username, email=self.normalize_email(email), first_name=first_name,last_name=last_name, **extra_fields)
        user.set_password(password) #Hashing Password

        user.save()
        return user

    def create_superuser(self,username, email, password=None):
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email")

        user = self.create_user(username=username, email=self.normalize_email(email))
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password) #Hashing Password

        user.save()
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def token(self):
        return ''
