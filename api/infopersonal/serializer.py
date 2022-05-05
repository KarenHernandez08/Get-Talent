from rest_framework import serializers 
#from vacantes.models import AreasModel, PreguntasModel, RolesModel, VacantesModel         
from infopersonal.models import InfoPesonalModel

#Construye tu serializador aquí
class InfoPersonalRegistoSerializer(serializers.ModelSerializer):
        class Meta:
                models = InfoPesonalModel
                fields = '__all__' 
