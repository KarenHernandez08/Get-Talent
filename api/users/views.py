from ast import Try
from asyncio import exceptions
from email import message
from django.shortcuts import render 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.models import UserModel
from users.serializers import UserSignupSerializer
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
import jwt



# Create your views here.
class UserSignupView(APIView):
    
    def post(self, request):
        data =request.data
        serializer = UserSignupSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
      
      #token  
        user_data=serializer.data
        user=UserModel.objects.get(email=user_data['email'])
        token=RefreshToken.for_user(user).access_token
        current_site=get_current_site(request).domain
        relative_link=reverse('email-verify')
        absurl='http://'+ current_site +relative_link+"?token="+ str(token)
        email_body='Hola, Selecciona el siguiente link para verificar tu correo.\n'+absurl
        data={'email_body':email_body, 'to_email':user.email, 'email_subject': 'Verifica tu correo'}

        
        Util.send_email(data)
        return Response({'message':"Succesfully"},status=status.HTTP_201_CREATED)
    
  
#Verificar Email y activacion de cuenta
class VerifyEmail(APIView):
    def get(self, request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token,settings.SECRET_KEY, algorithms='HS256')
            user=UserModel.objects.get(id=payload['user_id'])
            
            if not user.is_verified:
                user.is_verified=True
                user.save()
            
        
            if not user.is_active:
                user.is_active=True
                user.save()
            return Response({'email':'Succeesfully activated'},status=status.HTTP_200_OK)
        
        except jwt.ExpiredSignatureError as identifier:
            return Response({'email':'Activation Expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'email':'Invalid token'},status=status.HTTP_400_BAD_REQUEST)
        