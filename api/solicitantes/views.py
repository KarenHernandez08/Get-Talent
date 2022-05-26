from telnetlib import STATUS
from wsgiref.util import request_uri
from django.shortcuts import render 
from django.contrib.sites.shortcuts import get_current_site #para poder opbtener el dominio
from django.urls import reverse
from django.conf import settings #importamos la configuracion para usar el SECRET KEY
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from solicitantes.models import VideoSolicitanteModel

from solicitantes.models import InfoPesonalModel #para poder crear los 

from .renderers import SolicitantesRenderer
from users.models import User
from solicitantes.serializer import (
    InfoPersonalSerializer,
    VideoSolicitanteSerializer,
)

# Create your views here.
class InfoPersonalRegistroView(generics.GenericAPIView): 
    permission_classes = [permissions.AllowAny]
    renderer_classes = (SolicitantesRenderer,)
    queryset = InfoPesonalModel.objects.all() 
    serializer_class = InfoPersonalSerializer
    def post(self, request, usuario_id):
        usuario_instance = User.objects.get(id=usuario_id)
        es_empleador = usuario_instance.is_empleador
        try:
            data =request.data
            serializer = InfoPersonalSerializer(data=data)
            if es_empleador == True:
                return Response('Eres Empleador. No tienes autorización.', status=status.HTTP_401_UNAUTHORIZED)
            elif es_empleador == False:
                return Response('Autorización de Solicitante exitosa', status=status.HTTP_200_OK)
            serializer = InfoPersonalSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response('Información de Usuario Registrada', status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoSolicitanteView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = (SolicitantesRenderer,)
    serializer_class = VideoSolicitanteSerializer
    def post(self, request, usuario_id):
        usuario_instance = User.objects.get(id=usuario_id)
        es_empleador = usuario_instance.is_empleador
        try:
            data =request.data
            serializer = InfoPersonalSerializer(data=data)
            if es_empleador == True:
                return Response('Eres Empleador. No tienes autorización.', status=status.HTTP_401_UNAUTHORIZED)
            elif es_empleador == False:
                return Response('Autorización de Solicitante exitosa. Video Guardado', status=status.HTTP_200_OK)
            serializer = VideoSolicitanteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
