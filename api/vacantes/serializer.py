from rest_framework import serializers  
from dataclasses import fields
from users.serializers import IsEmpleadorSerializer
from vacantes.models import (
    PreguntasModel, 
    VacantesModel,
    RolesModel, 
    AreasModel
)

class VacantesSerializer (serializers.ModelSerializer):
    class Meta:
        model = VacantesModel
        fields = '__all__'
    
    def validate(self, attr):
        return attr
    
class PreguntasSerializer (serializers.ModelSerializer):
    class Meta:
        model = PreguntasModel
        fields = '__all__'
    
    def validate(self, attr):
        return attr


class PreguntasVacantesSerializer (serializers.ModelSerializer):
    preguntasmodel = PreguntasSerializer(many=True)
    es_empleador = IsEmpleadorSerializer (read_only=True)
    #vacante_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PreguntasModel.objects.all())

    class Meta:
        model = VacantesModel
        fields = '__all__'
        fields = ['localidad','modalidad','tipo_trabajo','descripcion','preguntasmodel','es_empleador']
        #DUDAS CON EL ES EMPLEADOR TENGO QUE REVISARLOO
    
    def create(self, validated_data):
        #Obtengo el contenido de orden_details
        preguntasmodel_data = validated_data.pop('preguntasmodel')
        #creamos el nuevo registro de la vacante
        nueva_vacante = VacantesModel.objects.create(**validated_data)
        
        #En un ciclo recorremos el preguntasmodel y creamos el nuevo registro
        for preguntasmodel in preguntasmodel_data:
            PreguntasModel.objects.create(**preguntasmodel, vacante_id=nueva_vacante)
        return nueva_vacante

class RolesSerializer (serializers.ModelSerializer):
    class Meta:
        model = RolesModel
        fields = '__all__'
    def validate(self, attr):
        return attr

class AreasSerializer (serializers.ModelSerializer):
    class Meta:
        model = AreasModel
        fields = '__all__'
    def validate(self, attr):
        return attr