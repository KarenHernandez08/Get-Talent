from django.urls import path
from postulaciones.views import PostulacionesView
urlpatterns = [
    path('users/vacantes/<int:vacante_id>/', PostulacionesView.as_view()),

]