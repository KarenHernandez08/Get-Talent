from rest_framework import serializers
from empleador.models import InfoEmpleadorModel
from .models import *

class InfoEmpleadorSerializers(serializers.ModelSerializer):
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.save()
        return instance
    
    class Meta:
        model = InfoEmpleadorModel
        fields =  ['name', 'description', 'logo']
