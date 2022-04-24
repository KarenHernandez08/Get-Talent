from django.urls import path, include
from vacantes.views import SoloAreasRegistroView, SoloPreguntasRegistroView, SoloRolesRegistroView, SoloVacantesRegistroView, VacantesRegistroView


urlpatterns = [
    path('user_company/vacantes/', VacantesRegistroView.as_view()),
    ###path('/user_company/<int:user_id>/vacantes', VacantesRegistroView.as_view()),
    ##La linea se cambiará cuando se tenga ya el registro de los usuarios

    #DE PRUEBA Y CONTROL
    path('solo/vacantes/', SoloVacantesRegistroView.as_view()),
    path('solo/roles/', SoloRolesRegistroView.as_view()),
    path('solo/areas/', SoloAreasRegistroView.as_view()),
    path('solo/preguntas/',  SoloPreguntasRegistroView.as_view()),  
]