
from rest_framework import serializers
from .models import *



class PostulacionesSerializer (serializers.ModelSerializer):
    
    
    class Meta:
        model = Postula
        fields = ['video', 'user_id', 'vacante_id']