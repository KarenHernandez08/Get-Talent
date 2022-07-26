
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
        

# Envio de email para contactar a l solcitante postulado
class ContactarPostulanteSerializer(serializers.Serializer):
    id_postulacion = serializers.PrimaryKeyRelatedField( queryset=Postula.objects.all())
    id_user = serializers.PrimaryKeyRelatedField( queryset=User.objects.all()) 
    #mensaje = serializers.CharField(max_length=600)
    #asunto = serializers.CharField(max_length=100)
    class Meta:
        fields = ['id_postulacion','id_user']
        
    def validate(self, data ):
        postulado_instancia = data.get('id_postulacion')
        id_postulacion = postulado_instancia.id
        empleador_instancia = data.get('id_user')
        #mensaje=data.get('mensaje')
        #asunto = data.get('asunto')
        if Postula.objects.filter(id=id_postulacion).exists():
            #Información de solicitante
            #postulado_instancia = Postula.objects.get(id_postulacion = id)
            #print("INFO SOLICITANTE")
            solicitante_id = postulado_instancia.user_id_id
            #print("id_solicitante",solicitante_id)
            email_solicitante = User.objects.get(id=solicitante_id)
            #print("solicitante instancia",solicitante_instancia)
            #email_solicitante = solicitante_instancia.email
            #print("email_solicitante",email_solicitante)
            solicitante_name = InfoPesonalModel.objects.get(user_id_id=solicitante_id)
            #print("instancia personal", solcitante_info)
            #solicitante_name = solcitante_info.name
            #print("name",solicitante_name)
            #Empresa informacion 
            #print("EMPRESA INFORMACION")
            vacante_id_id = postulado_instancia.vacante_id_id
            #print("vacante id",vacante_id_id)
            #vacante_instancia = VacantesModel.objects.get(vacante_id_id = 3)
            #print("Vacante instancia",vacante_instancia)
            #print("empleador instancia",empleador_instancia)
            email_empleador = empleador_instancia.email
            #print("emplador email",email_empleador)
            id_empresa = empleador_instancia.id
            #print("empresa id",id_empresa)
            company_instancia = InfoEmpleadorModel.objects.get(user_id_id = id_empresa)
            company_name = company_instancia.empresa
            #print("namecompany ",company_name)
            body= f"""Hola, {solicitante_name },
              La compañía {company_name} esta interesada en tí,
              para la vacante que te postulaste {vacante_id_id}.
              contactala en este email: {email_empleador}
              ¡Mucha suerte! 
              
              Valentis.Get-Talent"""
            data = {
                'email_subject':'Seguimiento Postulación GET-TALENT',
                'email_body':body,
                'to_email':email_solicitante
            }
            Util.send_email(data)
            print("envie el correo")
            return data
            # data = {
            #     'email_subject': asunto,
            #     'email_body': mensaje,
            #     'to_email':email_solicitante
            # }

class PostulanteMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
    def validate(self, attr):
        return attr
