from django.urls import path, include

from solicitantes.views import (
    InfoPersonalRegistroView, 
    VideoSolicitanteView, 
    InfoAcademicaView,
    InteresView,
    InformacionView,
    SolicitantesPostulacionesView
)

urlpatterns = [
    path('users/', InfoPersonalRegistroView.as_view()),
   
    path('users/videosolicitante/', VideoSolicitanteView.as_view()),

    path('users/infoacademica/', InfoAcademicaView.as_view()),
    
    path('users/interes/', InteresView.as_view()),
    
    path('users/informacion/', InformacionView.as_view()),
    
    path('users/postulaciones/', SolicitantesPostulacionesView.as_view())
] 
    