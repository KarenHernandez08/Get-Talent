from telnetlib import STATUS
from wsgiref.util import request_uri
from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site #para poder opbtener el dominio
from django.urls import reverse
from django.conf import settings #importamos la configuracion para usar el SECRET KEY
from django.contrib.auth import authenticate

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions
from vacantes.models import VacantesModel

from vacantes.serializer import VacantesSerializer

from postulaciones.models import Postula
from postulaciones.serializers import PostulacionesSerializer


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
        users = request.user
        print(users)
        obtener_id=users.id
        informacion_perso = bool(InfoPesonalModel.objects.filter(user_id = obtener_id))
        print(informacion_perso)
        informacion_acade = bool(InfoAcademicaModel.objects.filter (user_id = obtener_id).order_by('user_id'))
        print(informacion_acade)
        video_solicita = bool(VideoSolicitanteModel.objects.filter (user_id = obtener_id))
        print(video_solicita)
        interes = bool(InteresModel.objects.filter(user_id = obtener_id))
        print (interes)
        
        try:
            
            """informacion_personal = InfoPesonalModel.objects.get(user_id = obtener_id)
            informacion_academica = InfoAcademicaModel.objects.filter (user_id = obtener_id).order_by('user_id')
            video_solicitante = VideoSolicitanteModel.objects.get (user_id = obtener_id)
            intereses = InteresModel.objects.get (user_id = obtener_id)
            
            serializer = InfoPersonalSerializer(informacion_personal)
            serializer2 = InfoAcademicaSerializer(informacion_academica,  many = True)
            serializer3 = VideoSolicitanteSerializer(video_solicitante)
            serializer4 = InteresSerializer (intereses)"""
            
            if informacion_perso == False:
                if informacion_acade == False:
                    if  video_solicita == False :
                        if interes == False:
                           
                            
                            return Response ('Aun no tienes información')
            
            if informacion_perso == True:
                if informacion_acade == False:
                    if  video_solicita == False :
                        if interes == False:
                            informacion_personal = InfoPesonalModel.objects.get(user_id = obtener_id)
                            serializer = InfoPersonalSerializer(informacion_personal)
                            return Response({'Información Personal':serializer.data})
                        
            if informacion_perso == False:
                if informacion_acade == True:
                    if  video_solicita == False :
                        if interes == False: 
                            informacion_academica = InfoAcademicaModel.objects.filter (user_id = obtener_id).order_by('user_id')
                            serializer2 = InfoAcademicaSerializer(informacion_academica,  many = True)
                            return Response({'Información Academica':serializer2.data})
            
            if informacion_perso == False:
                if informacion_acade == False:
                    if  video_solicita == True :
                        if interes == False:
                            
                            video_solicitante = VideoSolicitanteModel.objects.get (user_id = obtener_id)
                            serializer3 = VideoSolicitanteSerializer(video_solicitante)
                            
                            return Response({'Video': serializer3.data})
                        
            if informacion_perso == False:
                if informacion_acade == False:
                    if  video_solicita == False :
                        if interes == True:
    
                            intereses = InteresModel.objects.get (user_id = obtener_id)
                            serializer4 = InteresSerializer (intereses)
                            return Response({'Intereses': serializer4.data})
                        
            if informacion_perso == True:
                if informacion_acade == True:
                    if  video_solicita == False :
                        if interes == False:
                            informacion_personal = InfoPesonalModel.objects.get(user_id = obtener_id)
                            informacion_academica = InfoAcademicaModel.objects.filter (user_id = obtener_id).order_by('user_id')
                            
                            serializer = InfoPersonalSerializer(informacion_personal)
                            serializer2 = InfoAcademicaSerializer(informacion_academica,  many = True)
                            
                            return Response({
                                'Información Personal':serializer.data, 
                                'Información Academica':serializer2.data})
            
            if informacion_perso == True:
                if informacion_acade == True:
                    if  video_solicita == True :
                        if interes == False:
                            informacion_personal = InfoPesonalModel.objects.get(user_id = obtener_id)
                            informacion_academica = InfoAcademicaModel.objects.filter (user_id = obtener_id).order_by('user_id')
                            video_solicitante = VideoSolicitanteModel.objects.get (user_id = obtener_id)
                            
                            serializer = InfoPersonalSerializer(informacion_personal)
                            serializer2 = InfoAcademicaSerializer(informacion_academica,  many = True)
                            serializer3 = VideoSolicitanteSerializer(video_solicitante)
                            
                            
                            return Response({
                                'Información Personal':serializer.data, 
                                'Información Academica':serializer2.data,
                                'Video': serializer3.data,
                                })
                            
            if informacion_perso == True:
                if informacion_acade == False:
                    if  video_solicita == False:
                        if interes == True:
                            informacion_personal = InfoPesonalModel.objects.get(user_id = obtener_id)
                            intereses = InteresModel.objects.get (user_id = obtener_id)
                            
                            serializer = InfoPersonalSerializer(informacion_personal)
                            serializer4 = InteresSerializer (intereses)
                            
                            return Response({
                                'Información Personal':serializer.data,
                                'Intereses': serializer4.data})
                            
            
            if informacion_perso == True:
                if informacion_acade == True:
                    if  video_solicita == True :
                        if interes == True:
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
             
            
      
        except:
            return Response ('Falta información por llenar')
          
          
class SolicitantesPostulacionesView (generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        users = request.user
        obtener_id= users.id
        print (obtener_id)
        
        postulaciones = Postula.objects.filter(user_id = obtener_id).first()
        print(postulaciones)
        
        """for x in postulaciones:
            print(x.vacante_id)"""
        
        
        #vacante = VacantesModel.objects.filter(vacante_id = postulaciones.vacante_id)
        #print(type(vacante))
        #vacantes= Postula.objects.all()
        vacante = VacantesModel.objects.all().filter(vacante_id= postulaciones.vacante_id).order_by('vacante_id')
        
        
        #vacante = Postula.objects.filter(vacante_id = post.vacante_id)
        
        serializer = PostulacionesSerializer(postulaciones, many=True)
        serializer2 = VacantesSerializer(vacante, many =True)
        
        return Response({
            'video':serializer.data,
            'vacante':serializer2.data
            
            
            })

    
    
   
