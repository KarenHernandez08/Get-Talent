from rest_framework import serializers

from users.models import UserModel
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework.exceptions import ValidationError

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        
    def validate(self, data):
            user = UserModel(**data)
            password = data.get('password')
            errors = dict() 
            confirm_password = data.get('confirmPassword')
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"

            if len(password) <6 or len(password) > 20:
               raise ValidationError('La contraseña debe tener mínimo 6 y no más de 20 de caracteres de longitud. ')

            if password != confirm_password:
               raise ValidationError('La contraseña debe coincidir.')

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

            try:
             validators.validate_password(password=password, user=user)
         
            except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)
         
            if errors:
             raise serializers.ValidationError(errors)
        
            return super(UserSignupSerializer, self).validate(data)
