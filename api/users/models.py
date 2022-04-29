#nativos
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, name, email, password=None, **kwargs):
        
        user = self.model(name=name, email=self.normalize_email(email),**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email, password=None, **kwargs):
        

        user=self.model(name=name, email=self.normalize_email(email),**kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff=True
        user.save()
        return user
    
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_empleador = models.BooleanField(default=False)
    
    
    
    USERNAME_FIELD= "email"
    REQUIRED_FIELDS=["name"]
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
#login  
"""    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }"""
