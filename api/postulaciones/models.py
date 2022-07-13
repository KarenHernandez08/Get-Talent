from django.db import models
from users.models import User
from vacantes.models import VacantesModel

# Create your models here.

class Postula(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, default = '') 
    vacante_id= models.ForeignKey(VacantesModel, on_delete=models.CASCADE, default = '')
    video = models.URLField(max_length = 200 , unique = True)
    

    

  