
from django.db import models
from users.models import User
from vacantes.choices import (TIPO_TRABAJO, MODALIDAD,
                             NIVEL_EXPERIENCIA,ESTADOS, AREAS) 


class VacantesModel(models.Model):
    vacante_id= models.BigAutoField(auto_created=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length = 150)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,default='', verbose_name= 'Empresa') 
    descripcion = models.TextField ( max_length=500)
    requisitos = models.TextField ( max_length=300)
    sueldo = models.DecimalField (default="0.0",max_digits=30 , decimal_places=2) 
    tipo_trabajo = models.CharField(max_length=30, choices=TIPO_TRABAJO)
    modalidad = models.CharField(max_length=20, choices=MODALIDAD)
    estado = models.CharField(max_length=25, choices=ESTADOS)
    area = models.CharField(max_length=60, choices=AREAS)
    experiencia = models.CharField(max_length=60, choices=NIVEL_EXPERIENCIA)
    vacante_video = models.CharField ( blank = True, max_length=150)
    #Esta sub clase me sirve para que Django nombre la tabla si no la tomara como la app y el modelo
    # class Meta:
    #     db_table = 'Vacantes'

    def __str__(self):
        return self.is_active

class PreguntasModel(models.Model):
    preguntas_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    pregunta1 = models.CharField(max_length=150)
    pregunta2 = models.CharField(max_length=150)
    pregunta3 = models.CharField(max_length=150)
    vacante_id= models.OneToOneField(VacantesModel, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     db_table = 'Preguntas para Vacantes'