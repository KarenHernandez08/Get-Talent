from django.db import models
from users.models import User

# Create your models here.

class InfoEmpleadorModel(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, default='', verbose_name= 'Empresa_id', null= False) #cambiar a user_id o lo que se decida
    empresa=models.CharField(max_length=50)
    description=models.TextField(max_length=500)
    logo=models.URLField(max_length=1000,blank = True)

   

