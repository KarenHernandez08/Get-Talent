from dataclasses import fields
from rest_framework import serializers  
from vacantes.models import (
    AreasModel, 
    PreguntasModel, 
    RolesModel, 
    VacantesModel  
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
    vacantes = VacantesSerializer(many=True)
    pregunta1 = serializers.CharField(max_length=150)
    pregunta2 = serializers.CharField(max_length=150)
    pregunta3 = serializers.CharField(max_length=150)

    class Meta:
        model = PreguntasModel
        fields = ['pregunta1','pregunta2','pregunta3','vacantes']

# class PreguntasVacantesSerializer(serializers.ModelSerializer):
#     owner = VacantesSerializer(read_only=True)
#     vacantes_ids = serializers.PrimaryKeyRelatedField (write_only=True,
#     queryset=VacantesModel.objects.all(), source='owner')
#     class Meta:
#         model = PreguntasModel
#         fields = ('preguntas_id','pregunta1','pregunta2','pregunta3','owner','vacantes_ids')

#     # def to_representation(self, instance):
#         # return{
#         #     'vacante_id':instance.vacante_id,
#         #     'pregunta1': instance.pregunta1,
#         #     'pregunta2': instance.pregunta2,
#         #     'pregunta3': instance.pregunta3,
#         #     'descripcio':instance.VacantesModel.descripcion,
#         #     'requisitos':instance.VacantesModel.requisitos,
#         # }
#         # return super().to_representation(
#         #     instance.vacante_id,
#         #     instance.pregunta1,
#         #     instance.pregunta2,
#         #     instance.pregunta3,
#         #     instance.VacantesModel.descripcion,
#         #     instance.VacantesModel.requisitos,
#         # )


#     def validate(self, attr):
#         return attr


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