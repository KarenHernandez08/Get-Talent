from rest_framework import serializers  
from users.serializers import IsEmpleadorSerializer
from vacantes.models import (
    PreguntasModel, 
    VacantesModel
)

class VacantesSerializer (serializers.ModelSerializer):
    class Meta:
        model = VacantesModel
        fields = ['vacante_id', 'is_active', 'name', 'descripcion', 'requisitos', 'sueldo', 'tipo_trabajo',
                  'modalidad', 'estado', 'area', 'experiencia', 'user_id']
    
    def validate(self, attr):
        return attr
    
class PreguntasSerializer (serializers.ModelSerializer):
    class Meta:
        model = PreguntasModel
        fields = ['pregunta1', 'pregunta2', 'pregunta3', 'vacante_id']
    
    def validate(self, attr):
        return attr

class PreguntasVacantesSerializer (serializers.ModelSerializer):
    preguntasmodel = PreguntasSerializer(many=True)
    #vacante_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PreguntasModel.objects.all())

    class Meta:
        model = VacantesModel
        
        fields = ['name','tipo_trabajo','descripcion','preguntasmodel','sueldo', 'requisitos', 'modalidad', 'vacante_video', 'estado', 'area', 'experiencia', 'user_id']
        
    
    def create(self, validated_data):
        #Obtengo el contenido de orden_details
        preguntasmodel_data = validated_data.pop('preguntasmodel')
        #creamos el nuevo registro de la vacante
        nueva_vacante = VacantesModel.objects.create(**validated_data)
        
        #En un ciclo recorremos el preguntasmodel y creamos el nuevo registro
        for preguntasmodel in preguntasmodel_data:
            PreguntasModel.objects.create(**preguntasmodel, vacante_id=nueva_vacante)
        return nueva_vacante

