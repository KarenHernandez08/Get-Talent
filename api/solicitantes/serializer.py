from dataclasses import fields
from rest_framework import serializers  
#from vacantes.models import AreasModel, PreguntasModel, RolesModel, VacantesModel         
from solicitantes.models import InfoPesonalModel

#Construye tu serializador aquí
class InfoPersonalRegistoSerializer(serializers.ModelSerializer):
        class Meta:
                models = InfoPesonalModel
                fields = '__all__' 


# class InfoPersonalRegistroSerializador(serializers.Modelserializer):
#         class Meta:
#            model = InfoPesonalModel
#            fields = '__all__'
    