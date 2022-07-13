from django.urls import path
from vacantes.views import VacantesFilterListModalidad
from vacantes.views import VacantesFilterListEstado, VacantesFilterListExperiencia, VacantesFilterListTipo

from vacantes.views import (
    SoloPreguntasRegistroView,  
    VacantesRegistroView,
    VacantesListView,
    VacantesFilterList,
    VacantesFilterListArea,
    VacantesFilterListNombre
)
urlpatterns = [
    ##path('user_company/vacantes/', VacantesRegistroView.as_view()),
    path('user_company/vacantes/', VacantesRegistroView.as_view()),
    ##La linea se cambiará cuando se tenga ya el registro de los usuarios

    #DE PRUEBA Y CONTROL
    path('solo/vacantes/', VacantesRegistroView.as_view()),
    path('solo/preguntas/',  SoloPreguntasRegistroView.as_view()),  
    path('vacantes/', VacantesListView.as_view()),
    path('vacantes/<int:vacante_id>/', VacantesFilterList.as_view()),
    path('vacantes/area/<str:area>/', VacantesFilterListArea.as_view()),
    path('vacantes/estado/<str:estado>/', VacantesFilterListEstado.as_view()),
    path('vacantes/tipo_trabajo/<str:tipo_trabajo>/', VacantesFilterListTipo.as_view()),
    path('vacantes/experiencia/<str:experiencia>/', VacantesFilterListExperiencia.as_view()),
    path('vacantes/modalidad/<str:modalidad>/', VacantesFilterListModalidad.as_view()),
    path('vacantes/nombre/<str:name>/', VacantesFilterListNombre.as_view()),
    
    
]
