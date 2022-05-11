from django.shortcuts import render
from telnetlib import STATUS
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions

from empleador.serializer import InfoEmpleadorSerializers 
from empleador.renderers import EmpleadorRenderer

# Create your views here. crear Post historia 9
class InfoEmpleadorPostView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]#para saber que permisos tiene y quien la pyede usar
    renderer_classes = (EmpleadorRenderer,)#autodocumentar en el swagger
    serializer_class = InfoEmpleadorSerializers

    def post(self, request):#Crear y guardar información
        serializer = InfoEmpleadorSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)#Respuesta para sabe si esta bien



