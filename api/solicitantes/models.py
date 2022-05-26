from django.core.validators import MaxValueValidator, MinValueValidator 
from django.db import models
from unicodedata import name
from users.models import User


# Create your models here.
class InfoPesonalModel(models.Model):
    name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    paternal_lastname = models.CharField(max_length=30)
    maternal_lastname = models.CharField(max_length=30)
    date_birth = models.DateField (default="0000-00-00", null = True, blank = False) #Checar 2018-06-29
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16), MaxValueValidator(100)])
    additional_mail = models.EmailField(max_length=50, default='null',null=True) ####CHECAR !!!!! 
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    
    # Propongo que sea un email adicional, pero el default sea el otro que ya dieron... 
    ## o simplemente eliminar ese campo 
    # que sea un campo para actualizar email

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
        
class VideoSolicitanteModel(models.Model):
    video = models.URLField(max_length=2000 , unique=True)

    def __str__(self):
        return self.video   
