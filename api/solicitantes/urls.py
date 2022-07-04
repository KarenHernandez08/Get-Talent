from django.urls import path, include
from users.models import User
from solicitantes.views import (
    InfoPersonalRegistroView, VideoSolicitanteView, InfoAcademicaView,
)

urlpatterns = [
    path('users/', InfoPersonalRegistroView.as_view()),
   
    path('users/videosolicitante', VideoSolicitanteView.as_view()),

    path('users/infoacademica', InfoAcademicaView.as_view()),
] 