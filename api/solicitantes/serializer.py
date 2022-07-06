from dataclasses import fields
from rest_framework import serializers
from users.serializers import IsEmpleadorSerializer
from solicitantes.models import (
    InfoPesonalModel, VideoSolicitanteModel, InfoAcademicaModel
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