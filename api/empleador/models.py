from django.db import models
from users.models import User

# Create your models here.

class InfoEmpleadorModel(models.Model):
    #empleador_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True, verbose_name= 'Empresa') #cambiar a user_id o lo que se decida
    name=models.CharField(max_length=50)
    description=models.TextField(max_length=500)
    logo=models.URLField(max_length=200)

    class Meta:
        db_table = 'Empleador'

