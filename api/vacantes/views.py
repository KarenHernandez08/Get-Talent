from django.shortcuts import render 
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions

from vacantes.renderers import VacantesRenderer
from vacantes.serializer import  (
    PreguntasVacantesSerializer,
    PreguntasSerializer,
    VacantesSerializer
)
from vacantes.models import (
    PreguntasModel, 
    VacantesModel
)

#Define tus vistas aquí
class SoloPreguntasRegistroView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (VacantesRenderer,)
    serializer_class = PreguntasSerializer
    def post(self, request):
        serializer = PreguntasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VacantesRegistroView(generics.GenericAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (VacantesRenderer,)
    serializer_class = PreguntasVacantesSerializer
    def post(self, request):
        data= request.data
        usuario_instance = request.user
        empresa= usuario_instance.id
        print(empresa)
        id_usuario =data.get('user_id')
        print ('id', id_usuario)
        es_empleador = usuario_instance.is_empleador
        try:
            serializer = PreguntasVacantesSerializer(data=request.data)
            if es_empleador == False:
                return Response('No tienes autorización para crear una vacante', status=status.HTTP_401_UNAUTHORIZED)
            elif es_empleador == True:
                if id_usuario == empresa:
                    serializer = PreguntasVacantesSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response('Autorización de Empleador Exitosa. Información de Vacante Registrada', status=status.HTTP_201_CREATED)
                return Response('No se puede guardar la informcaición')
        except:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          
    
class VacantesListView(generics.GenericAPIView):
    permission_classes= [permissions.IsAuthenticated]  
    
    def get(self, request):
        
        vacante= VacantesModel.objects.all()
        preguntas= PreguntasModel.objects.filter(pk__in = vacante)
        serializer =VacantesSerializer(vacante, many=True)
        serializer2 =PreguntasSerializer(preguntas, many=True)
        return Response({'vacantes':serializer.data, 
                         'preguntas':serializer2.data})

#filtrar por parametros
class VacantesFilterList(generics.GenericAPIView):
    permission_classes= [permissions.IsAuthenticated]
    
    def get(self, request, vacante_id):
        vacante=VacantesModel.objects.filter(vacante_id= vacante_id)
        preguntas= PreguntasModel.objects.filter(vacante_id=vacante_id)
        
        serializer = VacantesSerializer(vacante, many=True)
        serializer2 = PreguntasSerializer(preguntas, many=True)
        return Response({'vacantes':serializer.data, 
                         'preguntas':serializer2.data})
    
 
class VacantesFilterListArea(generics.GenericAPIView): 
    permission_classes= [permissions.IsAuthenticated]
    
    def get(self, request, area):
        area= VacantesModel.objects.filter(area__iexact=area)
        serializer = VacantesSerializer(area, many=True)
        return Response(serializer.data)
    
class VacantesFilterListEstado(generics.GenericAPIView): 
    permission_classes= [permissions.IsAuthenticated]
    
    def get(self, request, estado):
        estado = VacantesModel.objects.filter(estado__iexact=estado)
        serializer = VacantesSerializer(estado, many=True)
        return Response(serializer.data)
    
class VacantesFilterListTipo(generics.GenericAPIView): 
    permission_classes= [permissions.IsAuthenticated]
    
    def get(self, request, tipo_trabajo):
        print(tipo_trabajo)
        tipo_trabajo= VacantesModel.objects.filter(tipo_trabajo__iexact=tipo_trabajo)
        serializer= VacantesSerializer(tipo_trabajo, many=True)
        return Response(serializer.data)

class VacantesFilterListExperiencia(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, experiencia):
        experiencia = VacantesModel.objects.filter(experiencia__iexact = experiencia)
        serializer= VacantesSerializer(experiencia, many = True)
        return Response( serializer.data)

class VacantesFilterListModalidad(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, modalidad):
        modalidad = VacantesModel.objects.filter(modalidad__iexact = modalidad)
        serializer= VacantesSerializer(modalidad, many = True)
        return Response( serializer.data)

class VacantesFilterListNombre(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, name):
        name = VacantesModel.objects.filter(name__iexact = name)
        serializer= VacantesSerializer(name, many = True)
        return Response( serializer.data)


        
    
