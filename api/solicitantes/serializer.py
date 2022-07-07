from dataclasses import field, fields
from urllib import response
from rest_framework import serializers
from users.serializers import IsEmpleadorSerializer
from solicitantes.models import (
    InfoPesonalModel,
    InteresModel,
)

class InfoPersonalSerializer(serializers.ModelSerializer):
    es_empleador = IsEmpleadorSerializer (read_only=True)
    #vacante_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PreguntasModel.objects.all())
    class Meta:
        model = InfoPesonalModel
        fields = '__all__'




'''
class AreaSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = AreaModel
        fields = '__all__'
    def validate(self, atrr):
        return atrr



class RolSerializer(serializers.ModelSerializer):

    class Meta:
        model = RolModel
        fields = '__all__'
    
    def to_representation(self, instance):#Convertir el id en json
        responce = super().to_representation(instance)
        response['area_rol'] = AreaSerializer(instance.area).data
        return responce

    def validate(self, attrs):
        return attrs
'''

class InteresSerializer(serializers.ModelSerializer):
    es_empleador = IsEmpleadorSerializer (read_only=True)

    class Meta:
        model = InteresModel
        fields = '__all__'

    
'''    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['area_interes'] = InteresSerializer(instance.area_interes).data()
        response['rol_interes'] = InteresSerializer(instance.rol_interes).data()
        return response

    def validate(self, attrs):
        return attrs

'''

