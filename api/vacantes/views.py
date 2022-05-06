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
from rest_framework_simplejwt.tokens import RefreshToken #para poder crear los 

from .renderers import VacantesRenderer

from vacantes.serializer import  AreasSerializer, RolesSerializer, VacantesSerializer , PreguntasSerializer
from vacantes.models import VacantesModel , PreguntasModel, RolesModel, AreasModel


# Create your views here.
class SoloVacantesRegistroView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (VacantesRenderer,)
    serializer_class = VacantesSerializer
    def post(self, request):
        serializer = VacantesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SoloPreguntasRegistroView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (VacantesRenderer,)
    serializer_class = PreguntasSerializer
    def post(self, request):
        serializer = PreguntasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SoloAreasRegistroView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (VacantesRenderer,)
    serializer_class = AreasSerializer
    def post(self, request):
        serializer = AreasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SoloRolesRegistroView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (VacantesRenderer,)
    serializer_class = RolesSerializer
    def post(self, request):
        serializer = RolesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VacantesRegistroView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (VacantesRenderer,)
    serializer_class = PreguntasSerializer, VacantesSerializer
    def post(self, request):
        serializers_preguntas = PreguntasSerializer(data=request.data)
        print(serializers_preguntas)
        serializers_preguntas.is_valid(raise_exception=True)
        serializers_preguntas.save()

        serializers_vacantes = VacantesSerializer(data=request.data)
        print(serializers_vacantes)
        serializers_vacantes.is_valid(raise_exception=True)
        serializers_vacantes.save()
        
        return Response(status=status.HTTP_201_CREATED)