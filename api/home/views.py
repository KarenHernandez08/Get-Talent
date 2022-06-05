from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

# Create your models here.

class InicioAPIView(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response('Inicio', status=status.HTTP_200_OK)


        