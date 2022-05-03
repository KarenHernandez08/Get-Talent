from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.
class InfoPesonalModel(models.Model):
    name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    paternal_lastname = models.CharField(max_length=30)
    maternal_lastname = models.CharField(max_length=30)
    date_birth = models.DateTimeField ()
    age = models.PositiveSmallIntegerField(default=29, validators=[MinValueValidator(16), MaxValueValidator(100)])
    additional_mail = models.CharField(max_length=30) ####CHECAR

    class Gender_List(models.Choices):
        FEMENINO = "femenino"
        MASCULINO = "masculino"
        OTRO = "otro"
        SINESPECIFICAR = "sin especificar"
    gender = models.CharField(max_length=20, choices=Gender_List.choices, default='sin especificar')

    class Marital_List(models.Choices):
        SOLTERO = "soltero"
        CASADO = "casado"
        OTRO = "otro"
        SINESPECIFICAR = "sin especificar"
    marital_status = models.CharField(max_length=20, choices=Marital_List.choices, default='sin especificar')

   



    def __str__(self): 
        return self.name
    