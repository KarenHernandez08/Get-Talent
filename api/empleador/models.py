from django.db import models
from users.models import User

# Create your models here.

class InfoEmpleadorModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', verbose_name= 'Empresa_id') #cambiar a user_id o lo que se decida
    name=models.CharField(max_length=50)
    description=models.TextField(max_length=500)
    logo=models.URLField(max_length=1000, default='null', blank=True)

    class Meta:
        db_table = 'Empleador'

