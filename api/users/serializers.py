from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
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
    
    class Meta:
        fields = ['old_password','new_password']

    def validate(self, data ):
        new_password = data.get('new_password')
        user = self.context.get('user')
        special_characters = "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?¿"

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
        fields = ['email']

    def validate(self, attrs, request):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            print(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Token', token)
            current_site=get_current_site(request).domain
            relative_link=reverse('reset-password')
            link ='http://localhost:8000/reset-password/'+ uid+ '/'+token
            print(' Link', link)
            # Send EMail
            body = 'Click para cambiar contraseña '+link
            data = {
                'subject':'Cambiar contraseña',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('El usuario no esta registrado')

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise ValidationError("Las contraseñas no coinciden")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('El token no es valido o a expirado')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('El token no es valido o a expirado')
            
        
    