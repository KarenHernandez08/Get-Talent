from random import choices
from django.db import models
from unicodedata import name

from django.forms import CharField  
from users.models import User
from solicitantes.choices import (
    MODALIDAD, 
    TIPO_TRABAJO, 
    ESTADOS,
    AREAS,
    NIVEL_EXPERIENCIA,
)


class VacantesModel(models.Model):
    vacante_id= models.BigAutoField(auto_created=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    descripcion = models.TextField ( max_length=500)
    requisitos = models.TextField ( max_length=300)
    localidad = models.CharField ( default = 'No aplica' ,max_length=30)
    vacante_video = models.CharField ( max_length=150)
    sueldo = models.DecimalField (default="0.0",max_digits=30 , decimal_places=2)

    modalidad = models.CharField(max_length=20, choices=MODALIDAD)
    tipo_trabajo = models.CharField(max_length=20, choices=TIPO_TRABAJO)
    estado = models.CharField(max_length=25, choices=ESTADOS)
    area = models.CharField(max_length=60, choices=AREAS)
    #experiencia = CharField(max_length=60, choices=NIVEL_EXPERIENCIA)

    
    #Esta sub clase me sirve para que Django nombre la tabla si no la tomara como la app y el modelo
    class Meta:
        db_table = 'Vacantes'

    def __str__(self):
        return self.is_active


class PreguntasModel(models.Model):
    preguntas_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    pregunta1 = models.CharField(max_length=150)
    pregunta2 = models.CharField(max_length=150)
    pregunta3 = models.CharField(max_length=150)
    vacante_id= models.ForeignKey(VacantesModel, on_delete=models.CASCADE,null=True)
    #status= models.BooleanField(default=False) #¿Qué es? 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Preguntas para Vacantes'

