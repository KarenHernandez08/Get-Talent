
from rest_framework import serializers
from .models import *



class PostulacionesSerializer (serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(write_only = True, queryset = User.objects.all())
    vacante_id=serializers.PrimaryKeyRelatedField(write_only = True, queryset = VacantesModel.objects.all())
    
    class Meta:
        model = Postula
        fields = '__all__'