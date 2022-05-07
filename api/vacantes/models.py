from django.db import models
from unicodedata import name
from users.models import User

# from enum import Enum, unique
# @unique
# import enum
# CONTENDRA TODA LA INFORMACIÓN DE ESTA APLICACION QUE IRA A LA BD...
class AreasModel(models.Model):
    areas_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    status = models.BooleanField(default=False)
    nombre_area = models.CharField ( max_length=150)

    class Meta:
        db_table = 'Áreas de Interes'

class RolesModel(models.Model):
    rol_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    rol = models.CharField ( max_length=150)

    class Meta:
        db_table = 'Roles'

class InteresesAreasModel(models.Model):
    interesesareas_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False) 
    areas_id = models.ForeignKey(AreasModel, on_delete=models.CASCADE, null=True) 

    class Meta:
        db_table = 'Intereses por Área'

class RolAreasModel(models.Model):
    rolareas_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False) 
    interesesareas_id = models.ForeignKey(InteresesAreasModel, on_delete=models.CASCADE, null=True) 
    rol_id = models.ForeignKey(RolesModel, on_delete=models.CASCADE, null=True) 

    class Meta:
        db_table = 'Roles por Área'

class VacantesModel(models.Model):
    vacante_id= models.BigAutoField(auto_created=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    descripcion = models.TextField ( max_length=500)
    requisitos = models.TextField ( max_length=300)
    localidad = models.CharField ( default = 'No aplica' ,max_length=30)
    vacante_video = models.CharField ( max_length=150)
    sueldo = models.DecimalField ( max_digits=30 , decimal_places=2) 
    
    ##empleador_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True, verbose_name= 'Empresa') #cambiar a user_id o lo que se decida
    area_id = models.ForeignKey (AreasModel, on_delete=models.CASCADE , null=True)     #tabla externa
    roles_id = models.ForeignKey (RolesModel, on_delete=models.CASCADE, null=True)   #tabla externa

    class Modalidad_Lista(models.Choices):
        TIEMPO_COMPLETO = "Tiempo Completo"
        MEDIO_TIEMPO = "Medio Tiempo"
        PROYECTO = "Proyecto"
    tipo_trabajo = models.CharField(max_length=20, choices=Modalidad_Lista.choices)

    class Modalidad_Lista(models.Choices):
        PRESENCIAL = "Presencial"
        VIRTUAL = "Virtual"
        HIBRIDO = "Hibrido"
    modalidad = models.CharField(max_length=20, choices=Modalidad_Lista.choices)
      #con el color rojo es el que llamo a mi body ... 
    
    class Estados_Lista(models.Choices):
        AGUASCALIENTES = "Aguascalientes"
        BAJA_CALIFORNIA = "Baja California"
        BAJA_CALIFORNIA_SUR = "Baja California Sur"
        CAMPECHE = "Campeche"
        CHIAPAS = "Chiapas"
        CHIHUAHUA = "Chihuahua"
        CD_MEX = "Ciudad de México"
        COAHUILA = "Coahuila"
        COLIMA = "Colima"
        DURANGO = "Durango"
        GUANAJUATO = "Guanajuato"
        GUERRERO = "Guerrero"
        HIDALGO = "Hidalgo"
        JALISCO = "Jalisco"
        EDO_MEX = "Estado de México"
        MICHOACAN = "Michoacán"
        MORELOS = "Morelos"
        NAYARIT = "Nayarit"
        NUEVO_LEON = "Nuevo León"
        OAXACA = "Oaxaca"
        PUEBLA = "Puebla"
        QUERETARO = "Querétaro"
        QUINTANA_ROO = "Quintana Roo"
        SAN_LUIS_POTOSI = "San Luis Potosí"
        SINALOA = "Sinaloa"
        SONORA = "Sonora"
        TABASCO = "Tabasco"
        TAMAULIPAS = "Tamaulipas"
        TLAXCALA = "Tlaxcala"
        VERACRUZ = "Veracruz"
        YUCATAN = "Yucatán"
        ZACATECAS = "Zacatecas"
    localidad = models.CharField(max_length=25, choices=Estados_Lista.choices)

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

    status= models.BooleanField(default=False) #¿Qué es? 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Preguntas para Vacantes'

class VacantesAreasModel(models.Model):
    vacantesareas_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    vacante_id = models.ForeignKey(VacantesModel, on_delete=models.CASCADE,null=True)
    areas_id = models.ForeignKey(AreasModel, on_delete=models.CASCADE, null=True) 

    class Meta:
        db_table = 'Vacantes por Área'

class RolVacantesModel(models.Model):
    rolvacante = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    vacantesareas_id = models.ForeignKey(VacantesAreasModel, on_delete=models.CASCADE, null=True)
    rol_id = models.ForeignKey(RolesModel, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Roles para Vacantes'
