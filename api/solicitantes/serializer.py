from dataclasses import fields
from rest_framework import serializers
from users.serializers import IsEmpleadorSerializer
from solicitantes.models import (
    InfoPesonalModel, VideoSolicitanteModel, InfoAcademicaModel
)

class InfoPersonalSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = InfoPesonalModel
        fields = '__all__'

class VideoSolicitanteSerializer (serializers.ModelSerializer):
    
    class Meta: 
        model = VideoSolicitanteModel
        fields = '__all__'
        

class InfoAcademicaSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = InfoAcademicaModel
        fields = '__all__'