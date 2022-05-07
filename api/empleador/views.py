from django.shortcuts import render
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
from rest_framework_simplejwt.tokens import RefreshToken
from empleador.serializer import InfoEmpleadorSerializers #para poder crear los
from empleador.renderers import EmpleadorRenderer

# Create your views here. crear Post historia 9

class InfoEmpleadorPostView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]#para saber que permisos tiene y quien la pyede usar
    renderer_classes = (EmpleadorRenderer,)#autodocumentar en el swagger
    serializer_class = InfoEmpleadorSerializers

    def post(self, request):#Crear y guardar información
        serializer = InfoEmpleadorSerializers(data=request.data)
        serializer.is_valid(raise_excepetion=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)#Respuesta para sabe si esta bien



