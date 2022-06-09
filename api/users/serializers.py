from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
            uid = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link ='http://localhost:8000/reset-password/'+ uid+ '/'+token + '/'
            print(' Link', link)
            # Send EMail
            body = 'Hola, solicitaste el cambio de tu contraseña, solo dale click aquí '+ link
            data = {
                'email_subject':'Instrucciones para cambiar contraseña',
                'email_body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            if user.is_verified== False:
                raise serializers.ValidationError('Necesita verificar su email antes')
                  
            return attrs
            
        else:
            raise serializers.ValidationError('El usuario no esta registrado')
    

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    confirmPassword=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['new_password', 'confirmPassword']

    def validate(self, data):
        try:
            new_password = data.get('new_password')
            confirmPassword=data.get('confirmPassword')
            special_characters = "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?¿"
            uid = self.context.get('uid')
            token = self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('El token no es valido o a expirado')
            
            if new_password != confirmPassword:
                raise ValidationError('Las contraseñas no coiciden')

            if len(new_password) <6 or len(new_password) > 20:
                raise ValidationError('La contraseña debe tener mínimo 6 y no más de 20 de caracteres de longitud.')

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
            user.intentos=0
            user.is_active=True
            user.save()
            return data
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('El token no es valido o a expirado')


    
    
    
