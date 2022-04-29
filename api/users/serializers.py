
from django.core import exceptions
#import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User




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
        
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"

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
    
    
        
        
        
        
       



    
    
    