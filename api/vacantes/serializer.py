from dataclasses import fields
from rest_framework import serializers  
from vacantes.models import AreasModel, InfoPesonalModel, PreguntasModel, RolesModel, VacantesModel    

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
    

class RolesSerializer (serializers.ModelSerializer):
    class Meta:
        model = RolesModel
        fields = '__all__'
    def validate(self, attr):
        return attr

class AreasSerializer (serializers.ModelSerializer):
    class Meta:
        model = InfoPesonalModel
        fields = '__all__'
    def validate(self, attr):
        return attr