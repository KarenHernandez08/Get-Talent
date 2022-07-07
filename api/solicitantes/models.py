from tkinter import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models

from django.forms import CharField
from users.models import User
from .choices import (
    GENDER,
    MARITAL, 
    MODALIDAD, 
    TIPO_TRABAJO,
    AREAS,
    NIVEL_EXPERIENCIA,
)

# Create your models here.
class InfoPesonalModel(models.Model):
    name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    paternal_lastname = models.CharField(max_length=30)
    maternal_lastname = models.CharField(max_length=30)
    date_birth = models.DateField (blank = True) #Checar 2018-06-29
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(100)])
    additional_mail = models.EmailField(max_length=50, default='null',null=True)####CHECAR !!!!! 
    gender = models.CharField(max_length=20, choices=GENDER, default='sin especificar')
    marital_status = models.CharField(max_length=20, choices=MARITAL, default='sin especificar') 
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, default='') 

    class Meta:
        db_table = 'Informacion Personal'
    
    def __str__(self): 
        return self.name
    
'''
class AreaModel(models.Model):
    nombre_area = models.CharField(max_length=150)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'Areas'


class RolModel(models.Model):
    nombre_rol = models.CharField(max_length=150)
    status = models.BooleanField(default=False)
    area_rol = models.ForeignKey(AreaModel, on_delete=models.CASCADE, related_name='area_rol')
    
    class Meta:
        db_table = 'Roles'
'''

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




    