
from rest_framework import serializers
from empleador.models import InfoEmpleadorModel
from .models import *
from .serializer import *


class InfoEmpleadorSerializers(serializers.ModelSerializer):
    user_id=serializers.PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all())
    
    def update(self, instance, validated_data):
        instance.empresa = validated_data.get('empresa', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.save()
        return instance
        
    
    class Meta:
        model = InfoEmpleadorModel
        fields =  '__all__'
        
        
        #vacante_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PreguntasModel.objects.all())
