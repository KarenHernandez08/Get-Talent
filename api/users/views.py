from django.contrib.sites.shortcuts import get_current_site #para poder opbtener el dominio
from django.urls import reverse
from django.conf import settings #importamos la configuracion para usar el SECRET KEY
from django.contrib.auth import authenticate
from django.http import HttpResponsePermanentRedirect

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken #para poder crear los tokens
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import LoginSerializer, UserSignupSerializer, EmailVerificationSerializer, VerifySerializer, ChangePasswordSerializer, PasswordResetEmailSerializer, PasswordResetSerializer
from .utils import Util #importamos nuestra clase y metodo de enviar email
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer

import jwt
import os



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
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            email=serializer.data['email']
            password=serializer.data['password']
            user=authenticate(username=email, password=password)
            usuario_instance = User.objects.get(email=serializer.data['email']) #traigo mi usuario
            empleador=usuario_instance.is_empleador
            if usuario_instance.intentos==3:
                return Response('Cuenta Bloqueada, restablezca su contraseña', status=status.HTTP_401_UNAUTHORIZED)
            if usuario_instance.is_active == False:
                return Response('El usuario no esta activo', status=status.HTTP_401_UNAUTHORIZED)
            if usuario_instance.is_verified == False:
                return Response('El usuario no esta verificado', status=status.HTTP_401_UNAUTHORIZED)

            if user == None:
                N_intentos = usuario_instance.intentos
                print(N_intentos)
                if N_intentos < 3:
                    usuario_instance.intentos = N_intentos +1 
                    usuario_instance.save()

                if usuario_instance.intentos == 3: 
                    usuario_instance.is_active = False
                    usuario_instance.save()
                    return Response ('Cuenta bloqueada, vuelve a activarla', status=status.HTTP_503_SERVICE_UNAVAILABLE)

                return Response('Contraseña incorrecta, vuelva a intentarlo', status=status.HTTP_401_UNAUTHORIZED)
            else:
                usuario_instance.intentos = 0
                usuario_instance.save()
                tokens = get_tokens_for_user(user)
                    
                return Response({
                        'msg':'Exitosamente logueado',
                        'tokens':tokens,
                        'is_empleador':empleador
                    }, status=status.HTTP_200_OK)
        except:
            
            return Response({
                'msg':'Usuario no encontrado,vuelva a intentarlo'
            }, status=status.HTTP_400_BAD_REQUEST)
            
#verificar email 
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
            if user.is_verified  ==False:
                
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
                
            if  user.intentos == 3:
                return Response("Esta cuenta esta bloqueada", status=status.HTTP_400_BAD_REQUEST)
            if user.is_verified == True:
                return Response("Esta cuenta ya esta verificada", status=status.HTTP_400_BAD_REQUEST)
            
            return Response("Revise su correo para verificar su email", status=status.HTTP_200_OK)
            
    
        except:
            return Response("No hay una cuenta registraada con ese email", status=status.HTTP_400_BAD_REQUEST)

# Cambiar Contraseña
class ChangePasswordView(generics.GenericAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class= ChangePasswordSerializer
    
    def post(self, request, format=None):
        try:
            
            serializer = ChangePasswordSerializer(data=request.data, context={'user':request.user})
            serializer.is_valid(raise_exception=True)
            
            return Response('Contraseña cambiada correctamente', status=status.HTTP_200_OK)

        except:
            return Response('La acción no puede ejecurtarse en este momento', status=status.HTTP_400_BAD_REQUEST)

# Envio de email para recuperar contraseña
class PasswordResetEmailView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [UserRenderer]
    serializer_class=PasswordResetEmailSerializer
    def post(self, request, format=None):
        try:
            serializer = PasswordResetEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response('Revise su correo por favor ', status=status.HTTP_200_OK)
        
        except:
            return Response('El usuario no existe, coloque un correo valido', status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [UserRenderer]
    serializer_class=PasswordResetSerializer
    def post(self, request, uid, token, format=None):
        try:
            
            serializer = PasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
            serializer.is_valid(raise_exception=True)
            return Response('Nueva contraseña guardada con exito', status=status.HTTP_201_CREATED)
        except:
            return Response('El token ya expiro o los datos son incorrectos', status=status.HTTP_400_BAD_REQUEST)
    
    