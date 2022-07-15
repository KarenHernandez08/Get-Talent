
from rest_framework import serializers
from empleador.models import InfoEmpleadorModel
from .models import *
from users.serializers import *


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
        fields =  ['user_id', 'empresa', 'description', 'logo']
        
        def to_representation (self, instance):
        
            response= super().to_representation(instance)
            response['user_id']=UserSignupSerializer(instance.user_id).data
            return response 
        

    
