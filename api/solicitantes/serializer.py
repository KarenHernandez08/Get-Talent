from dataclasses import fields
from rest_framework import serializers
from users.serializers import IsEmpleadorSerializer
from solicitantes.models import (
    InfoPesonalModel, VideoSolicitanteModel, InfoAcademicaModel, InteresModel
)
from .models import *
from .serializer import * 


class InfoPersonalSerializer (serializers.ModelSerializer):
    user_id=serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all())
    
    class Meta:
        model = InfoPesonalModel
        fields = '__all__'

class VideoSolicitanteSerializer (serializers.ModelSerializer):
    user_id=serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all())
    
    class Meta: 
        model = VideoSolicitanteModel
        fields = '__all__'
        

class InfoAcademicaSerializer (serializers.ModelSerializer):
    user_id=serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all())
    
    class Meta:
        model = InfoAcademicaModel
        fields = '__all__'

class InteresSerializer(serializers.ModelSerializer):
    es_empleador = IsEmpleadorSerializer (read_only=True)

    class Meta:
        model = InteresModel
        fields = '__all__'