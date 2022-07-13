from telnetlib import STATUS
from wsgiref.util import request_uri
from django.shortcuts import render, get_object_or_404
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


from solicitantes.models import InfoPesonalModel
from solicitantes.models import InfoAcademicaModel
from solicitantes.models import VideoSolicitanteModel
from solicitantes.models import InteresModel

from .renderers import SolicitantesRenderer
from users.models import User
from solicitantes.serializer import (
    InfoPersonalSerializer,
    VideoSolicitanteSerializer,
    InteresSerializer,
    InfoAcademicaSerializer
)

# Create your views here.
class InfoPersonalRegistroView(generics.GenericAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (SolicitantesRenderer,)
    queryset = InfoPesonalModel.objects.all() 
    serializer_class = InfoPersonalSerializer
    
    def post(self, request):
        usuario_instance = request.user
        es_empleador = usuario_instance.is_empleador
        try:
            data =request.data
            serializer = InfoPersonalSerializer(data=data)
            if es_empleador == True:
                return Response('Eres Empleador. No tienes autorización.', status=status.HTTP_401_UNAUTHORIZED)
            elif es_empleador == False:
                serializer = InfoPersonalSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(' Autorización de Solicitante Exitosa. Información de Usuario Registrada', status=status.HTTP_201_CREATED)
        
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoSolicitanteView(generics.GenericAPIView):
    permission_classes =[permissions.IsAuthenticated]
    renderer_classes = (SolicitantesRenderer,)
    serializer_class = VideoSolicitanteSerializer
    
    def post(self, request):
        usuario_instance = request.user
        es_empleador = usuario_instance.is_empleador
        
        try:
            data =request.data
            serializer = InfoPersonalSerializer(data=data)
            if es_empleador == True:
                return Response('Eres Empleador. No tienes autorización.', status=status.HTTP_401_UNAUTHORIZED)
            elif es_empleador == False:
                serializer = VideoSolicitanteSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response('Autorización de Solicitante exitosa. Video Guardado', status=status.HTTP_200_OK)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfoAcademicaView(generics.GenericAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (SolicitantesRenderer,)
    queryset = InfoAcademicaModel.objects.all() 
    serializer_class = InfoAcademicaSerializer
    
    def post(self, request):
        usuario_instance = request.user
        es_empleador = usuario_instance.is_empleador
        
        try:
            data =request.data
            serializer = InfoAcademicaSerializer(data=data)
            if es_empleador == True:
                return Response('Eres Empleador. No tienes autorización.', status=status.HTTP_401_UNAUTHORIZED)
            elif es_empleador == False:
                serializer = InfoAcademicaSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response('Datos guardados correctamente', status=status.HTTP_201_CREATED)
        
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InteresView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (SolicitantesRenderer,)
    queryset = InteresModel.objects.all()
    serializer_class = InteresSerializer

    def post(self, request):
        usuario_instance = request.user
        es_empleador = usuario_instance.is_empleador
        
        try:
            data = request.data
            serializer = InteresSerializer(data=data)
            if es_empleador == True:
                return Response("Eres Empleador. No tienes autorización.", status=status.HTTP_401_UNAUTHORIZED)
            elif es_empleador == False:
                serializer = InteresSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response("Informacion de Intereses registrada.", status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class InformacionView (generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (SolicitantesRenderer,)
    queryset = InfoAcademicaModel.objects.all()
    
    def get(self,request):
          users=request.user
          print(users)
          obtener_id=users.id
          print(id)
          informacion_personal = InfoPesonalModel.objects.get(user_id = obtener_id)
          informacion_academica = InfoAcademicaModel.objects.filter (user_id = obtener_id).order_by('user_id')
          video_solicitante = VideoSolicitanteModel.objects.get (user_id = obtener_id)
          intereses = InteresModel.objects.get (user_id = obtener_id)
          
          serializer = InfoPersonalSerializer(informacion_personal)
          serializer2 = InfoAcademicaSerializer(informacion_academica,  many = True)
          serializer3 = VideoSolicitanteSerializer(video_solicitante)
          serializer4 = InteresSerializer (intereses)
          return Response({
              'Información Personal':serializer.data, 
              'Información Academica':serializer2.data,
              'Video': serializer3.data,
              'Intereses': serializer4.data})
    
