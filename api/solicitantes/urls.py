from django.urls import path, include
from users.models import User
from solicitantes.views import (
    InfoPersonalRegistroView, VideoSolicitanteView, InfoAcademicaView,
)

urlpatterns = [
    path('users/<int:usuario_id>/', InfoPersonalRegistroView.as_view()),
   
    path('users/<int:usuario_id>/videosolicitante', VideoSolicitanteView.as_view()),

    path('users/<int:usuario_id>/infoacademica', InfoAcademicaView.as_view()),
] 