
from django.contrib.sites.shortcuts import get_current_site #para poder opbtener el dominio
from django.urls import reverse
from django.conf import settings #importamos la configuracion para usar el SECRET KEY
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponsePermanentRedirect

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken #para poder crear los tokens

from users.models import User
from users.serializers import LoginSerializer, UserSignupSerializer, EmailVerificationSerializer, VerifySerializer,SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer
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

                if N_intentos >= 3: 
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
                        'tokens':tokens
                    }, status=status.HTTP_200_OK)
        except:
            
            return Response({
                'msg':'Usuario no encontrado,vuelva a intentarlo'
            }, status=status.HTTP_400_BAD_REQUEST)


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
                #en este caso que todo este correcto enviara un mensaje de exito 
            if  user.intentos == 3:
                return Response("Esta cuenta esta bloqueada", status=status.HTTP_400_BAD_REQUEST)
            if user.is_verified == True:
                return Response("Esta cuenta ya esta verificada", status=status.HTTP_400_BAD_REQUEST)
            
    
        except:
            return Response("No hay una cuenta registraada con ese email", status=status.HTTP_400_BAD_REQUEST)
        
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        
   
class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        password=request.data.get('password')
        confirmPassword=request.data.get('confirmPassword')
        if password != confirmPassword:
            return Response('Las contraseñas no coinciden', status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)     
  