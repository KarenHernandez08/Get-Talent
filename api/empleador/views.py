from django.shortcuts import render
from telnetlib import STATUS
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions
#from yaml import serialize

from users.models import User
from empleador.serializer import InfoEmpleadorSerializers 
from empleador.renderers import EmpleadorRenderer

# Create your views here. crear Post historia 9
class InfoEmpleadorPostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]#para saber que permisos tiene y quien la pyede usar
    renderer_classes = (EmpleadorRenderer,)#autodocumentar en el swagger
    serializer_class = InfoEmpleadorSerializers

    def post(self, request):#Crear y guardar información, el usuario_id vendrá dado desde el endpoint
        usuario_instance = request.user
        es_empleador = usuario_instance.is_empleador #aca traigo del usuario, solo el dado "is_empleador"
        try:
            serializer = InfoEmpleadorSerializers(data=request.data) #traigo la informacion del endpoint 
            if es_empleador == False:    # Si el usuario No es empleador 
                 return Response('No tienes autorización para subir Información de Empresas', status=status.HTTP_401_UNAUTHORIZED)
            elif es_empleador == True:  # Si el usuario Es empleador
                 return Response('Autorización de Empleador exitosa', status=status.HTTP_200_OK)
            serializer = InfoEmpleadorSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)  #valido la información
            serializer.save()                 # si todo va bien lo guardo
            return Response('Información de Vacante Registrada', status=status.HTTP_201_CREATED)
        except:
             # si no es valida ya dará información expecifica del error de la información
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)#Respuesta para sabe si esta bien



