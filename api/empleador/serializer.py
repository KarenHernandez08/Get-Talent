from rest_framework import serializers
from dataclasses import fields
from empleador.models import InfoEmpleadorModel

class InfoEmpleadorSerializers(serializers.ModelSerializer):
    #empleador_id = serializers.ForeignKey(User, on_delete=models.CASCADE,null=True, verbose_name= 'Empresa') #cambiar a user_id o lo que se decida
    #name=serializers.CharField(max_length=50)
    #description=serializers.TextField(max_length=500)
    #logo=serializers.URLField(max_length=200)

    class Meta:
        model = InfoEmpleadorModel
        fields = '__all__'