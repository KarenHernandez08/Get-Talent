

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

import random
import datetime
from datetime import timedelta
from datetime import datetime
from users.models import User   
from .utils import Util


#Registro
class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs={
            'password':{
                'write_only':True
            }
        }
        
    def validate(self, data):
            password = data.get('password')
        
            special_characters = "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?¿"

            if len(password) <6 or len(password) > 20:
               raise ValidationError('La contraseña debe tener mínimo 6 y no más de 20 de caracteres de longitud. ')


            if not any(x.isalpha() for x in password):
                raise ValidationError('La contraseña debe contener al menos una letra.')
         
            if not any(x.isupper() for x in password):
                raise ValidationError('La contraseña debe contener al menos una letra Mayúscula.')

            if not any(x.islower() for x in password):
                raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
        
            if not any(x.isdigit() for x in password):
                raise ValidationError('La contraseña debe de contener al menos un dígito del [0-9].')
          
            if not any(x in special_characters for x in password):
                raise ValidationError('La contraseña debe contener al menos un caracter especial.')

            return data
        
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        user.save()
        return user
    
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

#login
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=50)
    password=serializers.CharField(max_length=100)
    
    class Meta:
        model=User
        fields=[
            'email',
            'password'
        ]
        
#verificar email        
class VerifySerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=50)
    
    class Meta:
        model=User
        fields=['email']
        
class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    confirmPassword=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['new_password', 'confirmPassword']
        
    def validate(self, data ):
        new_password = data.get('new_password')
        confirmPassword=data.get('confirmPassword')
        user = self.context.get('user')
        special_characters = "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?¿"
        
        if new_password != confirmPassword:
                raise ValidationError('Las contraseñas no coiciden')

        if len(new_password) <6 or len(new_password) > 20:
            raise ValidationError('La contraseña debe tener mínimo 6 y no más de 20 de caracteres de longitud. ')

        if not any(x.isalpha() for x in new_password):
            raise ValidationError('La contraseña debe contener al menos una letra.')
         
        if not any(x.isupper() for x in new_password):
            raise ValidationError('La contraseña debe contener al menos una letra Mayúscula.')

        if not any(x.islower() for x in new_password):
            raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
        
        if not any(x.isdigit() for x in new_password):
            raise ValidationError('La contraseña debe de contener al menos un dígito del [0-9].')
          
        if not any(x in special_characters for x in new_password):
            raise ValidationError('La contraseña debe contener al menos un caracter especial.')
        
        user.set_password(new_password)
        user.save()
        return data

class IsEmpleadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_empleador',)
    def validate(self, attr):
        return attr
    
#######################################
# Envio de email para recuperar contraseña
class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            codigo_acceso = random.randint(1000, 9999) 
            link = str(codigo_acceso)
            print('codigo acceso', link)
            #GUARDAR CODIGO ACCESO MODELO
            # Send EMail
            # Send EMail
            body= f"""Hola,
              Tu código de acceso para cambiar tu contrseña es: 
              {link}
              Si no solicitaste este correo, por favor ignoralo. 
              Recuerda no compartir tus contraseñas.  
              
              Reuerda,¡Tu haces a Get Talent!
              Valentis.Get-Talent"""
            data = {
                'email_subject':'Cambio de contraseña',
                'email_body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            # Cambio de un registro modificando los campos llamando a save() a continuación.
            user.codigo_acceso = codigo_acceso
            creado=datetime.now()
            user.created_acceso= str(creado)
            user.save()
            if user.is_verified== False:
                raise serializers.ValidationError('Necesita verificar su email antes')
                  
            return attrs
            
        else:
            raise serializers.ValidationError('El usuario no esta registrado')

###############################################################
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    acceso_front=serializers.IntegerField()
    new_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    confirmPassword=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model=User
        fields = ['email','acceso_front','new_password', 'confirmPassword']

    def validate(self, data):
        email_front = data.get('email')
        acceso_front = data.get('acceso_front')
        new_password = data.get('new_password')
        confirmPassword = data.get('confirmPassword')
        special_characters = "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?¿"
        
        if User.objects.filter(email=email_front).exists():
            user = User.objects.get(email = email_front)
            codigo_acceso = user.codigo_acceso
            creado = user.created_acceso
            creado_time = datetime.strptime(creado, '%Y-%m-%d %H:%M:%S.%f')
            time_expiracion = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=5, hours=0, weeks=0)
            actual_time = datetime.now()
            
            if codigo_acceso == acceso_front: 
                if actual_time-creado_time > time_expiracion:
                    raise ValidationError('Expiro el tiempo genera otro token')
                elif actual_time-creado_time < time_expiracion:
                    if new_password != confirmPassword:
                            raise ValidationError('Las contraseñas no coiciden')

                    if len(new_password) <6 or len(new_password) > 20:
                        raise ValidationError('La contraseña debe tener mínimo 6 y no más de 20 de caracteres de longitud. ')

                    if not any(x.isalpha() for x in new_password):
                        raise ValidationError('La contraseña debe contener al menos una letra.')
                    
                    if not any(x.isupper() for x in new_password):
                        raise ValidationError('La contraseña debe contener al menos una letra Mayúscula.')

                    if not any(x.islower() for x in new_password):
                        raise ValidationError('La contraseña debe contener al menos una letra minúscula.')
                    
                    if not any(x.isdigit() for x in new_password):
                        raise ValidationError('La contraseña debe de contener al menos un dígito del [0-9].')
                    
                    if not any(x in special_characters for x in new_password):
                        raise ValidationError('La contraseña debe contener al menos un caracter especial.')
                    
                    user.set_password(new_password)
                    user.created_acceso(0) #Reiniciamos codigo de acceso
                    user.save()
                    return data
                    
            else: 
                print("Codigo invalido")
                #raise ValidationError('Codigo invalido')
           
            if user.is_verified== False:
                raise serializers.ValidationError('Necesita verificar su email antes')
        else:
            raise serializers.ValidationError('El usuario no esta registrado')

class CodigoSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    acceso_front=serializers.IntegerField()

    class Meta:
        model=User
        fields = ['email','acceso_front']

    def validate(self, data):
        email_front = data.get('email')
        acceso_front = data.get('acceso_front')
        
        if User.objects.filter(email=email_front).exists():
            user = User.objects.get(email = email_front)
            codigo_acceso = user.codigo_acceso
            creado = user.created_acceso
            creado_time = datetime.strptime(creado, '%Y-%m-%d %H:%M:%S.%f')
            time_expiracion = timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=9, hours=0, weeks=0)
            actual_time = datetime.now()
            
            if codigo_acceso == acceso_front: 
                if actual_time-creado_time > time_expiracion:
                    raise ValidationError('Expiro el tiempo genera otro token')
                elif actual_time-creado_time < time_expiracion:
                    print("Todo bien :D")
                    return data
            else: 
                raise ValidationError('Codigo invalido')


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('El Token ha expirado o es invalido')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
           
           
     