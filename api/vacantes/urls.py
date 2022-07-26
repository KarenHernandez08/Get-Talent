from django.urls import path


from vacantes.views import (
    SoloPreguntasRegistroView,  
    VacantesRegistroView,
    VacantesListView,
    VacantesFilterList,
    VacantesFilter
)
urlpatterns = [
    ##path('user_company/vacantes/', VacantesRegistroView.as_view()),
    path('user_company/vacantes/', VacantesRegistroView.as_view()),
    ##La linea se cambiará cuando se tenga ya el registro de los usuarios

    #DE PRUEBA Y CONTROL
    #path('solo/vacantes/', VacantesRegistroView.as_view()),
    #path('solo/preguntas/',  SoloPreguntasRegistroView.as_view()),  
    path('vacantes/', VacantesListView.as_view()),
    path('vacantes/<int:vacante_id>/', VacantesFilterList.as_view()),
    path('vacantes/<str:texto>/', VacantesFilter.as_view())
    
    
]
