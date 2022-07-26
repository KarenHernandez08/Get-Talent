from django.urls import path

from empleador.views import (
    ContactarPostulanteView,
    InfoEmpleadorPostView,
    EmpleadorPostulacionesView
)


urlpatterns = [ 
    path('empresa/contactar/<int:postulacion_id>/', ContactarPostulanteView.as_view()),
    path('empresa/informacion/', InfoEmpleadorPostView.as_view()),
    path('empresa/postulaciones/<int:vacante_id>/', EmpleadorPostulacionesView.as_view())
]