
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
from empleador.serializer import (ContactarPostulanteSerializer, InfoEmpleadorSerializers, 
PostulanteMailSerializer)
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
          
          obtener_id=users.id
          
          es_empleador = users.is_empleador #aca traigo del usuario, solo el dato "is_empleador"
          
          empleador=bool(InfoEmpleadorModel.objects.filter(user_id=obtener_id))
          print(empleador)
          vacantes= bool(VacantesModel.objects.filter (user_id = obtener_id, is_active=True).order_by('user_id'))
          print(vacantes)
          
          try:
               if es_empleador == False:    # Si el usuario No es empleador 
                    return Response('No tienes autorización', status=status.HTTP_401_UNAUTHORIZED)
               if empleador ==False:
                    if vacantes == False:
                         return Response('No se encontro ninguna información')
                    
               if es_empleador == True:
                    if empleador == True:
                         if vacantes ==False:
                              empleador=InfoEmpleadorModel.objects.get(user_id=obtener_id)
                              serializer=InfoEmpleadorSerializers(empleador)
                              return Response({
                                   'Información de la empresa':serializer.data
                                   })
               
               if es_empleador == True:
                    if empleador == False:
                         if vacantes ==True:
                         
                              vacantes= VacantesModel.objects.filter (user_id = obtener_id, is_active=True).order_by('user_id')
                              preguntas= PreguntasModel.objects.filter(pk__in = vacantes)
                              
                              serializer2 = VacantesSerializer(vacantes, many =True)
                              serializer3 = PreguntasSerializer(preguntas, many = True)
                                   
                              return Response({
                                   'Vacantes':serializer2.data,
                                   'Preguntas':serializer3.data
                                   })
                              
               
                    
               if es_empleador == True:
                    if empleador == True:
                         if vacantes ==True:
                         
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
          except:
               return Response('No se encontro ')
                         
          
               
          
class EmpleadorPostulacionesView(generics.GenericAPIView):
     permission_classes = [permissions.IsAuthenticated]
     def get(self,request, vacante_id):
          users=request.user
          print(users)
          obtener_id=users.id
          print(obtener_id)
          es_empleador = users.is_empleador 
          print(es_empleador)
          postulacion= bool(Postula.objects.filter(vacante_id = vacante_id))
          vacantes= bool(VacantesModel.objects.filter (user_id = obtener_id, vacante_id = vacante_id))
          print(vacantes)
          print (postulacion)
          #try:
          if es_empleador == False:    
                    return Response('No tienes autorización', status=status.HTTP_401_UNAUTHORIZED)
          elif es_empleador == True:
               if postulacion ==True:
                    if vacantes == True:
                         vacantes= VacantesModel.objects.filter (vacante_id = vacante_id)
                         preguntas= PreguntasModel.objects.filter(pk__in = vacantes)
                         postulacion= Postula.objects.filter(vacante_id = vacante_id)
                         
                         post = Postula.objects.filter(vacante_id = vacante_id)
                         
                         #solicitantes = InfoPesonalModel.objects.all().filter(name= post.user_id)
                         #print(solicitantes)
                              
                         #solicitante = InfoPesonalModel.objects.filter(pk= post.user_id).order_by('user_id')
                         solicitante = InfoPesonalModel.objects.all().get('user_id'). split(user_id =postulacion.user_id).order_by('user_id')
                              
                         serializer = VacantesSerializer(vacantes, many =True)
                         serializer2 = PreguntasSerializer(preguntas, many = True)
                         serializer3 = PostulacionesSerializer(postulacion, many = True)
                         serializer4 = InfoPersonalSerializer(solicitante, many =True)   
                         
                             
               else:
                    return Response('Aun nadie se postula a la vacante')
                    
                    
               return Response({
                    'Vacante':serializer.data, 
                    'Preguntas':serializer2.data,
                    'Solicitantes que se postularon':serializer4.data,
                    'videos':serializer3.data 
                    })
          #except:
               #return Response('No le corresponde la vacante')
                    

class ContactarPostulanteView(generics.GenericAPIView):
     permission_classes = [permissions.IsAuthenticated]#para saber que permisos tiene y quien la pyede usar
     renderer_classes = (EmpleadorRenderer,)#autodocumentar en el swagger
     serializer_class = ContactarPostulanteSerializer

     def post(self, request, postulacion_id):#Crear y guardar información, el usuario_id vendrá dado desde el endpoint
          usuario_instance = request.user#Aca llamo del modelo User la información del usuario con el id dado
          id_user=usuario_instance.id
          data = request.data
          id_usuario =data.get('user_id')

          es_empleador = usuario_instance.is_empleador #aca traigo del usuario, solo el dado "is_empleador"
         
          serializer = ContactarPostulanteSerializer(data=request.data) #traigo la informacion del endpoint
          try:
               if es_empleador == False:    # Si el usuario No es empleador 
                    return Response('No tienes autorización para subir Información de Empresas', status=status.HTTP_401_UNAUTHORIZED)
               elif es_empleador == True:
                    
                    serializer = ContactarPostulanteSerializer(data=request.data)
                    print("entre a la validacion")
                    serializer.is_valid(raise_exception=True)  #valido la información
                    print("pase la validacion")
                    return Response('Email automatico enviado al solicitante', status=status.HTTP_201_CREATED)
          except:
               return Response('Error', status=status.HTTP_400_BAD_REQUEST)#Respuesta para sabe si esta bien
     def get(self,request, postulacion_id):
          postulado_instancia = Postula.objects.get(id=postulacion_id)
          postulante = postulado_instancia.user_id_id
          print(postulado_instancia)

          solicitante_instancia = User.objects.filter(id=postulante)
          print(postulante)
          try: 
               
               serializer = PostulanteMailSerializer(solicitante_instancia, many=True)
               serializer.is_valid
               return Response(serializer.data, status=status.HTTP_200_OK)
          except:
               return Response('Error', status=status.HTTP_400_BAD_REQUEST)      

