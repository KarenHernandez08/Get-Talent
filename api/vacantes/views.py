from telnetlib import STATUS
from wsgiref.util import request_uri
from django.shortcuts import render 
from django.contrib.sites.shortcuts import get_current_site #para poder opbtener el dominio
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions

#from django.conf import settings #importamos la configuracion para usar el SECRET KEY
#from django.contrib.auth import authenticate
#from rest_framework_simplejwt.tokens import RefreshToken #para poder crear los 
#from rest_framework.permissions import AllowAny

from .renderers import VacantesRenderer

from vacantes.serializer import  AreasSerializer, PreguntasVacantesSerializer, RolesSerializer, VacantesSerializer , PreguntasSerializer
from vacantes.models import VacantesModel , PreguntasModel, RolesModel, AreasModel

#Define tus vistas aquí

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
    queryset = PreguntasModel.objects.all() 
    serializer_class = PreguntasVacantesSerializer
    def post(self, request):
        serializers = PreguntasVacantesSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        print("si valide")
        serializers.save()
        print(serializers)
        return Response(status=status.HTTP_201_CREATED)

