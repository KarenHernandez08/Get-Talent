from ast import Try
from asyncio import exceptions
from email import message
from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.models import UserModel
from users.serializers import UserSignupSerializer
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken #para poder crear los tokens
from .utils import Util #importamos nuestra clase y metodo de enviar email
from django.contrib.sites.shortcuts import get_current_site #para poder opbtener el dominio
from django.urls import reverse
from django.conf import settings #importamos la configuracion para usar el SECRET KEY
import jwt





# Create your views here.
class UserSignupView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        data =request.data
        serializer = UserSignupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
      
      #token  
        #esta variable solo obtiene el email de el usuario
        user=UserModel.objects.get(email=user_data['email'])
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
        return Response({'message':"Succesfully"},status=status.HTTP_201_CREATED) 
    
  
#Verificar Email y activacion de cuenta
class VerifyEmail(APIView):
    permission_classes = [permissions.AllowAny]
    #funcion para obtener el token
    def get(self, request):
        #Aqui obtenemos el token con el get
        token=request.GET.get('token')
        try:
            #intenta decodificar el token 
            payload=jwt.decode(token,settings.SECRET_KEY) 
            #despues de decodificar obtendremos los datos por el id del usuario
            user=UserModel.objects.get(id=payload['user_id'])
            
            #podremos ya cambiar el is_verified y el is_active  solo si el usuario no esta verificado
            if not user.is_verified:
                user.is_verified=True
                user.save()
            
        
            if not user.is_active:
                user.is_active=True
                user.save()
            return Response({'email':'Succeesfully activated'},status=status.HTTP_200_OK)
        
        #errores de activacion y errores de decodificacion de token 
        except jwt.ExpiredSignatureError as identifier:
            return Response({'email':'Activation Expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'email':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)