
from tracemalloc import get_object_traceback
from django.shortcuts import get_object_or_404, render


from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions
from solicitantes.models import InfoPesonalModel
from solicitantes.serializer import InfoPersonalSerializer

from postulaciones.serializers import PostulacionesSerializer
from postulaciones.models import Postula
from vacantes.serializer import PreguntasSerializer, VacantesSerializer

from vacantes.models import PreguntasModel

from vacantes.models import VacantesModel
from vacantes.serializer import PreguntasVacantesSerializer

#from yaml import serialize
from .models import *
from users.models import User
from empleador.models import InfoEmpleadorModel
from empleador.serializer import InfoEmpleadorSerializers
from empleador.renderers import EmpleadorRenderer

# Create your views here. crear Post historia 9
class InfoEmpleadorPostView(generics.GenericAPIView):
     permission_classes = [permissions.IsAuthenticated]#para saber que permisos tiene y quien la pyede usar
     renderer_classes = (EmpleadorRenderer,)#autodocumentar en el swagger
     serializer_class = InfoEmpleadorSerializers

     def post(self, request ):#Crear y guardar información, el usuario_id vendrá dado desde el endpoint
          usuario_instance = request.user#Aca llamo del modelo User la información del usuario con el id dado
          print("usuario instance",usuario_instance)
          id_user=usuario_instance.id
          data = request.data
          id_usuario =data.get('user_id')
          print ('id', id_usuario)
  
          es_empleador = usuario_instance.is_empleador #aca traigo del usuario, solo el dado "is_empleador"
          print(es_empleador)
          serializer = InfoEmpleadorSerializers(data=request.data) #traigo la informacion del endpoint
          try:
               if es_empleador == False:    # Si el usuario No es empleador 
                    return Response('No tienes autorización para subir Información de Empresas', status=status.HTTP_401_UNAUTHORIZED)
               elif es_empleador == True:
                    if id_usuario == id_user:
                         serializer = InfoEmpleadorSerializers(data=request.data)
                         serializer.is_valid(raise_exception=True)  #valido la información
                         serializer.save()                 # si todo va bien lo guardo
                         return Response('Autorización de Empleador Exitosa. Información de Compañia Registrada', status=status.HTTP_201_CREATED)
                    else:
                         return Response('El usuario es incorrecto', status = status.HTTP_400_BAD_REQUEST)        
                    
          except:
               return Response('Ya existe este usuario', status=status.HTTP_400_BAD_REQUEST)#Respuesta para sabe si esta bien

     def put(self, request, usuario_id, info_id):

         data = request.data
         usuario_id =data.get('user_id')
         print ('id', usuario_id)
         usuario_instance = User.objects.get(id=usuario_id) #Aca llamo del modelo User la información del usuario con el id dado
         es_empleador = usuario_instance.is_empleador #aca traigo del usuario, solo el dado "is_empleador"
         #infoempleador_instance = InfoEmpleadorModel.objects.get(id=info_id)
         infoempleador_instance = get_object_or_404(InfoEmpleadorModel, id=info_id)
         serializer = InfoEmpleadorSerializers(instance=infoempleador_instance, data=request.data, partial=True)
         serializer.is_valid(raise_exception=True) 
         serializer.save()
         return Response(serializer.data, status=status.HTTP_200_OK)
    
     def get(self,request):
          users=request.user
          print(users)
          obtener_id=users.id
          print(id)
          es_empleador = users.is_empleador #aca traigo del usuario, solo el dado "is_empleador"
          print(es_empleador)
          if es_empleador == False:    # Si el usuario No es empleador 
               return Response('No tienes autorización para subir Información de Empresas', status=status.HTTP_401_UNAUTHORIZED)
          elif es_empleador == True:
               empleador=InfoEmpleadorModel.objects.get(user_id=obtener_id)
               vacantes= VacantesModel.objects.filter (user_id = obtener_id, is_active=True).order_by('user_id')
               preguntas= PreguntasModel.objects.filter(pk__in = vacantes)
               serializer=InfoEmpleadorSerializers(empleador)
               serializer2 = VacantesSerializer(vacantes, many =True)
               serializer3 = PreguntasSerializer(preguntas, many = True)
               
               areas={'preguntas': serializer3.data}
               vacantes= {'Vacantes':serializer2.data}
               unir=dict(**vacantes, **areas)
               return Response({
                    'Información de la empresa':serializer.data, 
                    'Vacantes':serializer2.data,
                    'Preguntas':serializer3.data
                    })
          
class EmpleadorPostulacionesView(generics.GenericAPIView):
     permission_classes = [permissions.IsAuthenticated]
     def get(self,request, vacante_id):
          users=request.user
          print(users)
          obtener_id=users.id
          print(obtener_id)
          es_empleador = users.is_empleador 
          print(es_empleador)
          if es_empleador == False:    
               return Response('No tienes autorización', status=status.HTTP_401_UNAUTHORIZED)
          elif es_empleador == True:
               vacantes= VacantesModel.objects.filter (vacante_id = vacante_id)
               preguntas= PreguntasModel.objects.filter(pk__in = vacantes)
               postulacion= Postula.objects.filter(vacante_id = vacante_id)
               post = Postula.objects.filter(vacante_id = vacante_id).first()
               
               
               solicitante = InfoPesonalModel.objects.filter(user_id= post.user_id)
               #solicitante = InfoPesonalModel.objects.all().get('post.user_id').filter(user_id= post.user_id)
               
               
               serializer = VacantesSerializer(vacantes, many =True)
               serializer2 = PreguntasSerializer(preguntas, many = True)
               serializer3 = PostulacionesSerializer(postulacion, many = True)
               serializer4 = InfoPersonalSerializer(solicitante, many =True)
               
               
               return Response({
                    'Vacante':serializer.data, 
                    'Preguntas':serializer2.data,
                    'Postulantes':serializer3.data,
                    'user':serializer4.data
                    
                    })
               
               

