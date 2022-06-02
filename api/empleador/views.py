from tracemalloc import get_object_traceback
from django.shortcuts import get_object_or_404, render
from telnetlib import STATUS
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions

#from yaml import serialize

from users.models import User
from empleador.models import InfoEmpleadorModel
from empleador.serializer import InfoEmpleadorSerializers
from empleador.renderers import EmpleadorRenderer

# Create your views here. crear Post historia 9
class InfoEmpleadorPostView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]#para saber que permisos tiene y quien la pyede usar
    renderer_classes = (EmpleadorRenderer,)#autodocumentar en el swagger
    serializer_class = InfoEmpleadorSerializers

    def post(self, request, usuario_id):#Crear y guardar información, el usuario_id vendrá dado desde el endpoint
        usuario_instance = User.objects.get(id=usuario_id) #Aca llamo del modelo User la información del usuario con el id dado
        es_empleador = usuario_instance.is_empleador #aca traigo del usuario, solo el dado "is_empleador"
        try:
            serializer = InfoEmpleadorSerializers(data=request.data) #traigo la informacion del endpoint 
            if es_empleador == False:    # Si el usuario No es empleador 
                 return Response('No tienes autorización para subir Información de Empresas', status=status.HTTP_401_UNAUTHORIZED)
            elif es_empleador == True:  # Si el usuario Es empleador
                 serializer = InfoEmpleadorSerializers(data=request.data)
                 serializer.is_valid(raise_exception=True)  #valido la información
            serializer.save()                 # si todo va bien lo guardo
            return Response('Autorización de Empleador Exitosa. Información de Compañia Registrada', status=status.HTTP_201_CREATED)
        except:
             # si no es valida ya dará información expecifica del error de la información
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)#Respuesta para sabe si esta bien

    def put(self, request, usuario_id, info_id):
        usuario_instance = User.objects.get(id=usuario_id) #Aca llamo del modelo User la información del usuario con el id dado
        es_empleador = usuario_instance.is_empleador #aca traigo del usuario, solo el dado "is_empleador"
        #infoempleador_instance = InfoEmpleadorModel.objects.get(id=info_id)
        infoempleador_instance = get_object_or_404(InfoEmpleadorModel, id=info_id)
        serializer = InfoEmpleadorSerializers(instance=infoempleador_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

     #    try:
     #        serializer = InfoEmpleadorSerializers(data=request.data) 
     #        if es_empleador == False:    
     #             return Response('No tienes autorización para editar Información de Empresas', status=status.HTTP_401_UNAUTHORIZED)
     #        elif es_empleador == True:  
     #             request.data
     #             #infocompany_update = get_object_or_404(InfoEmpleadorModel, id=usuario_id)
     #             info_company = InfoEmpleadorModel.objects.filter(id=info_id)
     #             serializer = InfoEmpleadorSerializers(info_company, data=request.data)
     #        serializer.is_valid(raise_exception=True)  
     #        serializer.save()                 
     #        return Response('Autorización de Empleador Exitosa. Información de Compañia Editada', status=status.HTTP_201_CREATED)
     #    except:
     #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#NOTAAAAAAAAAAA COMO GUARDO EL USUARIO ASOCIADO ? EL ID EN EL SERIALIZADOR O LA VISTA 