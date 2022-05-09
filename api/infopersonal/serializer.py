from dataclasses import fields
from rest_framework import serializers  
from infopersonal.models import InfoPesonalModel

class InfoPersonalSerializer (serializers.ModelSerializer):
    class Meta:
        model = InfoPesonalModel
        fields = '__all__'
    