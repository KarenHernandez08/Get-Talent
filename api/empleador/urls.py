from django.urls import path

from empleador.views import (
    InfoEmpleadorPostView,
    EmpleadorPostulacionesView
)


urlpatterns = [ 
    path('empresa/informacion/', InfoEmpleadorPostView.as_view()),
    path('empresa/postulaciones/<int:vacante_id>/', EmpleadorPostulacionesView.as_view())
    
]