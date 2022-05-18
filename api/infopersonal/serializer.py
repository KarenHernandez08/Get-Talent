from dataclasses import fields
from rest_framework import serializers  
from infopersonal.models import InfoPesonalModel, VideoSolicitanteModel

class InfoPersonalSerializer (serializers.ModelSerializer):
    class Meta:
        model = InfoPesonalModel
        fields = '__all__'

class VideoSolicitanteSerializer (serializers.ModelSerializer):
    class Meta: 
        model = VideoSolicitanteModel
        fields = '__all__'
        