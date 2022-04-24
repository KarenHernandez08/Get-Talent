from telnetlib import STATUS
from wsgiref.util import request_uri
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from vacantes.serializer import  AreasSerializer, RolesSerializer, VacantesSerializer , PreguntasSerializer
from vacantes.models import VacantesModel , PreguntasModel, RolesModel, AreasModel


# Create your views here.
class SoloVacantesRegistroView(APIView): 
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = VacantesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SoloPreguntasRegistroView(APIView): 
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = PreguntasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SoloAreasRegistroView(APIView): 
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = AreasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SoloRolesRegistroView(APIView): 
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = RolesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VacantesRegistroView(APIView):
    permission_classes = (AllowAny, )
    
    def post(self, request):
        serializers_preguntas = PreguntasSerializer(data=request.data)
        print(serializers_preguntas)
        serializers_preguntas.is_valid(raise_exception=True)
        serializers_preguntas.save()


        serializers_vacantes = VacantesSerializer(data=request.data)
        print(serializers_vacantes)
        serializers_vacantes.is_valid(raise_exception=True)
        serializers_vacantes.save()
        # serializers = {
        #     'Preguntas': PreguntasSerializer(data=request.data),
        #     'Vacantes': VacantesSerializer(data=request.data)
        # }
        #if PreguntasSerializer:
        #serializers_preguntas.save()
        
    
        #if VacantesSerializer.is_valid():
        #    serializers_vacante.save()
        
        return Response(status=status.HTTP_201_CREATED)