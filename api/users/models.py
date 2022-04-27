from django.db import models
from enum import unique


# Create your models here.
class UserModel(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_empleador = models.BooleanField(default=False)
    confirmPassword = models.CharField(max_length=20)
    
    
    USERNAME_FIELD= "email"
def __str__(self):
        return self.email