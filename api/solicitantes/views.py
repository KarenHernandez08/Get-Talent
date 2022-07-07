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
from rest_framework_simplejwt.tokens import RefreshToken

from .renderers import SolicitantesRenderer
from users.models import User
from solicitantes.models import (
    InfoPesonalModel,
    InteresModel, 
    )
from solicitantes.serializer import (
    InfoPersonalSerializer,
    InteresSerializer,

    )

# Create your views here.
# class InfoPersonalRegistroView(generics.GenericAPIView): 
#     permission_classes = [permissions.AllowAny]
#     renderer_classes = (SolicitantesRenderer,)
#     serializer_class = InfoPersonalSerializer
#     def post(self, request):
#         serializer = InfoPersonalSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#####
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
                serializer = InfoPersonalSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response('Autorización de Solicitante Exitosa. Información de Usuario Registrada', status=status.HTTP_201_CREATED)

        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InteresView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (SolicitantesRenderer,)
    queryset = InteresModel.objects.all()
    serializer_class = InteresSerializer

    def post(self, request, usuario_id):
        usuario_instance = User.objects.get(id=usuario_id)
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
            return Response("Informacion de Intereses registrada.", status=status.HTTP_201_CREATED)
        
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        





'''
class AreaView(generics.GenericAPIView):#Crea un área
    permission_classes = [permissions.AllowAny]
    renderer_classes = (SolicitantesRenderer,)
    queryset = InteresModel.objects.all()
    serializer_class = AreaSerializer

    def post(self,request):
        data = request.data
        serializer = AreaSerializer(data=data)
        serializer.is_valid(raise_exception=True)#Devuelve automáticamente el código de error
        serializer.save()
        return Response({'message':'El área se creo correctamente'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        areas = AreaModel.objects.all().filter(statuss_delete=False)
        serializer = AreaSerializer(areas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SoloAreaView(generics.GenericAPIView):#Obtener solo un área
    permission_classes = [permissions.AllowAny]

    def get(self, request, area_id):
        area_obj = get_object_or_404(AreaModel, pk=area_id)
        serializer = AreaSerializer(area_obj)
        return Response(serializer.data)


class RolView(generics.GenericAPIView):#Crea el rol
    permission_classes = [permissions.AllowAny]
    renderer_classes = (SolicitantesRenderer,)
    queryset = InteresModel.objects.all()
    serializer_class = RolSerializer

    def post(self,request):
        data = request.data
        serializer = AreaSerializer(data=data)
        serializer.is_valid(raise_exception=True)#Devuelve automáticamente el código de error
        serializer.save()
        return Response({'message':'El rol se creo correctamente'}, status=status.HTTP_201_CREATED)

    def get(self, request):
        rol = RolModel.objects.all().filter(status_delete=False)
        serializer = RolModel(rol, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SoloRolView(generics.GenericAPIView):#Obtener solo un rol
    permission_classes = [permissions.AllowAny]
        
    def get(self, request, rol_id):
        rol_obj = get_object_or_404(RolModel, pk = rol_id)
        serializer = RolSerializer(rol_obj)
        return Response(serializer.data)
'''
