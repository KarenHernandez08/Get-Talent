from django.db import models

# Create your models here.
class InfoPesonalModel(models.Model):
    name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    paternal_lastname = models.CharField(max_length=30)
    maternal_lastname = models.CharField(max_length=30)
    date_birth = 
    age = 
    additional_mail= 
    marital_status = 



      def __str__(self):
         return self.name
    