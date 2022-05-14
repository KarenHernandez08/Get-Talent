from dataclasses import fields
from rest_framework import serializers  
from users.serializers import IsEmpleadorSerializer
from solicitantes.models import (
    InfoPesonalModel,
)

class InfoPersonalSerializer (serializers.ModelSerializer):
    es_empleador = IsEmpleadorSerializer (read_only=True)
    #vacante_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PreguntasModel.objects.all())
    class Meta:
        model = InfoPesonalModel
        fields = [
            'es_empleador','name','middle_name',
            'paternal_lastname','maternal_lastname',
            'age','additional_mail',
            'date_birth','gender','marital_status']
    