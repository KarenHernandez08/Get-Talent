from tkinter import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models

from django.forms import CharField
from users.models import User
from .choices import *

# Create your models here.
class InfoPesonalModel(models.Model):
    name = models.CharField(max_length = 30)
    middle_name = models.CharField(max_length = 30)
    paternal_lastname = models.CharField(max_length = 30)
    maternal_lastname = models.CharField(max_length = 30)
    date_birth = models.DateField (blank = True) 
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(100)])
    additional_mail = models.EmailField(max_length=50, default='null', blank = True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, default = '') 
    gender = models.CharField(max_length = 20, choices = GENDER, default = 'sin especificar')
    marital_status = models.CharField(max_length = 20, choices = MARITAL, default = 'sin especificar')

    def __str__(self): 
        return self.name
        
class VideoSolicitanteModel(models.Model):
    video = models.URLField(max_length=2000 , unique=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, default = '') 

    def __str__(self):
        return self.video   


class InfoAcademicaModel(models.Model): 
    name = models.CharField(max_length = 30)
    institucion = models.CharField(max_length = 100)
    fecha_inicio = models.DateField(default = "0000-00-00", null = True, blank = False)
    fecha_fin = models.DateField(default = "0000-00-00", null = True, blank = False)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, default = '' )
    nivel_escolar = models.CharField(max_length = 20, choices = NIVEL, default='sin especificar')
    estatus_academico = models.CharField(max_length=20, choices = ESTATUS, default='sin especificar')

    def __str__(self): 
     return self.name


class InteresModel(models.Model):
    
    modalidad = models.CharField(max_length=30, choices=MODALIDAD)
    tipo_trabajo = models.CharField(max_length=30, choices=TIPO_TRABAJO)
    area_interes = models.CharField(max_length=100, choices=AREAS)
    experiencia_interes = models.CharField(max_length=100, choices=NIVEL_EXPERIENCIA)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default= '')
   
    class Meta:
        db_table = 'Intereses'  
    def __int__(self): 
        return self.user_id