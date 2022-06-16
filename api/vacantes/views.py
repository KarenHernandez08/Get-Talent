from django.shortcuts import render 
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions

from users.models import User
from vacantes.renderers import VacantesRenderer
from vacantes.serializer import  (
    PreguntasVacantesSerializer,
    PreguntasSerializer,
    VacantesSerializer,
    AreasSerializer,
    RolesSerializer, 
)
from vacantes.models import (
    PreguntasModel, 
    VacantesModel,
    RolesModel, 
    AreasModel
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

# class VacantesRegistroView(generics.GenericAPIView):
#     permission_classes = [permissions.AllowAny]
#     renderer_classes = (VacantesRenderer,)
#     queryset = PreguntasModel.objects.all() 
#     serializer_class = PreguntasVacantesSerializer
#     def post(self, request):
#         serializers = PreguntasVacantesSerializer(data=request.data)
#         serializers.is_valid(raise_exception=True)
#         serializers.save()
#         print(serializers)
#         return Response(status=status.HTTP_201_CREATED)


class VacantesRegistroView(generics.GenericAPIView): 
    permission_classes = [permissions.AllowAny]
    renderer_classes = (VacantesRenderer,)
    serializer_class = PreguntasVacantesSerializer
    def post(self, request, usuario_id):
         usuario_instance = User.objects.get(id=usuario_id)
         es_empleador = usuario_instance.is_empleador
         try:
             data =request.data
             serializer = PreguntasVacantesSerializer(data=request.data)
             if es_empleador == False:
                 return Response('No tienes autorización para crear una vacante', status=status.HTTP_401_UNAUTHORIZED)
             elif es_empleador == True:
                 serializer = PreguntasVacantesSerializer(data=data)
             serializer.is_valid(raise_exception=True)
             serializer.save()
             return Response('Autorización de Empleador Exitosa. Información de Vacante Registrada', status=status.HTTP_201_CREATED)
         except:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SoloVacantesRegistroView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = (VacantesRenderer,)
    serializer_class = VacantesSerializer

    def get(self, request, usuario_id):
        vacante_obj = VacantesModel.objects.filter(empleador_id=usuario_id).first()
        #author_obj = get_object_or_404(Author,id=author_id)
        serializer = VacantesSerializer(vacante_obj)

        # vacantes_instancia = get_object_or_404(VacantesModel,empleador_id=usuario_id)
        # serializer = VacantesSerializer(vacantes_instancia)
        return Response(serializer.data, status=status.HTTP_200_OK)