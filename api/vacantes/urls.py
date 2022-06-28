from django.urls import path, include
from users.models import User
from vacantes.views import (
    SoloPreguntasRegistroView, 
    SoloVacantesRegistroView, 
    VacantesRegistroView,
)

urlpatterns = [
    ##path('user_company/vacantes/', VacantesRegistroView.as_view()),
    path('user_company/<int:usuario_id>/vacantes/', VacantesRegistroView.as_view()),
    ##La linea se cambiará cuando se tenga ya el registro de los usuarios

    #DE PRUEBA Y CONTROL
    path('solo/vacantes/<int:usuario_id>/', VacantesRegistroView.as_view()),
    path('solo/preguntas/',  SoloPreguntasRegistroView.as_view()),  
]