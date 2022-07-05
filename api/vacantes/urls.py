from django.urls import path, include
from users.models import User
from vacantes.views import (
    SoloPreguntasRegistroView, 
    SoloVacantesRegistroView, 
    VacantesRegistroView,
)

urlpatterns = [
    ##path('user_company/vacantes/', VacantesRegistroView.as_view()),
    path('user_company/vacantes/', VacantesRegistroView.as_view()),
    ##La linea se cambiará cuando se tenga ya el registro de los usuarios

    #DE PRUEBA Y CONTROL
    path('solo/vacantes/', VacantesRegistroView.as_view()),
    path('solo/preguntas/',  SoloPreguntasRegistroView.as_view()),  
]