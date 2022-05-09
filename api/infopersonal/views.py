from telnetlib import STATUS
from wsgiref.util import request_uri
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from infopersonal.serializer import InfoPersonalSerializer

# Create your views here.

class InfoPersonalRegistroView(APIView): 
    permission_classes = (AllowAny, )
    def post(self, request):
        serializer = InfoPersonalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

