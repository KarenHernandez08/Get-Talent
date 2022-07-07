from random import choices
from django.db import models
from users.models import User
from vacantes.choices import (TIPO_TRABAJO, MODALIDAD,
                             NIVEL_EXPERIENCIA,ESTADOS, AREAS) 

# CONTENDRA TODA LA INFORMACIÓN DE ESTA APLICACION QUE IRA A LA BD...
# class AreasModel(models.Model):
#     areas_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
#     nombre_area = models.CharField ( max_length=150)

#     def __str__(self):
#         return self.nombre_area
#     # class Meta:
#     #     db_table = 'Áreas de Interes'

# class RolesModel(models.Model):
#     rol_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
#     rol_name = models.CharField ( max_length=150)
#     area_id = models.ManyToManyField(AreasModel)

#     def __str__(self):
#         return self.rol_name
#     #Protect , no deja que un dato se elimine si este tiene un Area asignada

#     # class Meta:
#     #     db_table = 'Roles'

class VacantesModel(models.Model):
    vacante_id= models.BigAutoField(auto_created=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,default='', verbose_name= 'Empresa') 
    descripcion = models.TextField ( max_length=500)
    requisitos = models.TextField ( max_length=300)
    localidad = models.CharField ( default = 'No aplica' ,max_length=30)
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