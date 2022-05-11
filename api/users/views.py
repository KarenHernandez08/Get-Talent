
from ast import Return
from django.shortcuts import render 
from django.contrib.sites.shortcuts import get_current_site #para poder opbtener el dominio
from django.urls import reverse
from django.conf import settings #importamos la configuracion para usar el SECRET KEY
from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken #para poder crear los tokens
import jwt
from users.models import User
from users.serializers import LoginSerializer, UserSignupSerializer, EmailVerificationSerializer, VerifySerializer
from .utils import Util #importamos nuestra clase y metodo de enviar email
from django.http import HttpResponsePermanentRedirect
import os
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer



class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

# Create your views here.
class UserSignupView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (UserRenderer,)
    serializer_class = UserSignupSerializer
    def post(self, request):
        try:
            data =request.data
            
            password=data.get('password')
            confirmPassword=data.get('confirmPassword')
            if password != confirmPassword:
                return Response('Las contraseñas no coinciden', status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSignupSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data=serializer.data  
        
 
            #token  
            #esta variable solo obtiene el email de el usuario
            user=User.objects.get(email=user_data['email'])
            #definimos el token
            token=RefreshToken.for_user(user).access_token 
            #aqui ya lo ponemos para obtener la respuesta del dominio
            current_site=get_current_site(request).domain
            #para que regrese el link de urls.py para verificar email
            relative_link=reverse('email-verify')
            # la absurl se refiere al link que al usuario le llegara, en este caso el dominio mas el token para validar al usuario
            absurl='http://'+ current_site +relative_link+"?token="+ str(token) 
            #el mensaje que le llegara en el correo mas la absurl
            email_body='Hola, Selecciona el siguiente link para verificar tu correo.\n'+absurl 
            #Data que vamos a enviar a Util
            data={'email_body':email_body, 'to_email':user.email, 'email_subject': 'Verifica tu correo'}
 

            #aqui invocamos el metodo y mandamos la data para utils.py
            Util.send_email(data) 
            #en este caso que todo este correcto enviara un mensaje de exito 
            return Response('Usuario creado', status=status.HTTP_201_CREATED)
        
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
#Verificar Email y activacion de cuenta
class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [permissions.AllowAny]
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    #funcion para obtener el token
    def get(self, request):
        #Aqui obtenemos el token con el get
        token=request.GET.get('token')
        try:
            #intenta decodificar el token 
            payload=jwt.decode(token,settings.SECRET_KEY, algorithms='HS256') 
            #despues de decodificar obtendremos los datos por el id del usuario
            user=User.objects.get(id=payload['user_id'])
            
            #podremos ya cambiar el is_verified y el is_active  solo si el usuario no esta verificado
            if not user.is_verified:
                user.is_verified=True
                user.save()
            
        
            if not user.is_active:
                user.is_active=True
                user.save()
            return Response({'email':'Activado exitosamente'},status=status.HTTP_200_OK)
        
        #errores de activacion y errores de decodificacion de token 
        except jwt.ExpiredSignatureError as identifier:
            return Response({'email':'La activación expiro'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'email':'token Invalido'},status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }        
#Login
class LoginAPIView(generics.GenericAPIView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
  
  
    def post(self, request):
        try:
            serializer=LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email=serializer.data['email']
            password=serializer.data['password']
            user=authenticate(username=email, password=password)
            
            
            for user.intentos in range(3):
                    if password==password:
                            break
            if password==password:
                tokens = get_tokens_for_user(user)
                user.intentos=0
                user.save()
                
                return Response({
                'msg':'Exitosamente logueado',
                'tokens':tokens
            }, status=status.HTTP_200_OK)
            
            else:
                while password!=password:
                    user.intentos+=1
                    user.is_active=False
                    user.save()
                    return Response("Bloqueado", status=status.HTTP_400_BAD_REQUEST)
            
            
        except:
            if user is None:
                return Response('Credenciales invalidades', status=status.HTTP_401_UNAUTHORIZED)
            if user.is_active is None:
                return Response('El usuario no esta activo', status=status.HTTP_401_UNAUTHORIZED)
            if user.is_verified is None:
                return Response('El usuario no esta verificado', status=status.HTTP_401_UNAUTHORIZED)
            return Response('ERROR', status=status.HTTP_400_BAD_REQUEST)
            
            
            

class Verificar(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifySerializer
    def post(self, request):
        try:
            serializer = VerifySerializer(data=request.data)
            serializer.is_valid(raise_exception=True) 
            #token  
            #esta variable solo obtiene el email de el usuario
            user=User.objects.get(email=serializer.data['email'])
            if user.is_active==False:
                
                #definimos el token
                token=RefreshToken.for_user(user).access_token 
                #aqui ya lo ponemos para obtener la respuesta del dominio
                current_site=get_current_site(request).domain
                #para que regrese el link de urls.py para verificar email
                relative_link=reverse('email-verify')
                # la absurl se refiere al link que al usuario le llegara, en este caso el dominio mas el token para validar al usuario
                absurl='http://'+ current_site +relative_link+"?token="+ str(token) 
                #el mensaje que le llegara en el correo mas la absurl
                email_body='Hola, Selecciona el siguiente link para verificar tu correo.\n'+absurl 
                #Data que vamos a enviar a Util
                data={'email_body':email_body, 'to_email':user.email, 'email_subject': 'Verifica tu correo'}
    

                #aqui invocamos el metodo y mandamos la data para utils.py
                Util.send_email(data) 
                #en este caso que todo este correcto enviara un mensaje de exito 
                return Response('Activado correctamente', status=status.HTTP_201_CREATED)
            if user.intentos ==3:
                return Response('Tu cuenta esta bloqueada, por favor cambia tu contraseña', status=status.HTTP_400_BAD_REQUEST)
            if user.is_active==True:
                return Response("Esta cuenta ya esta activa", status=status.HTTP_400_BAD_REQUEST)
            
    
        except:
            return Response("No hay una cuenta registraada con ese email", status=status.HTTP_400_BAD_REQUEST)
        
        
  