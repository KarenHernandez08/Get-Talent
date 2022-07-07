from django.urls import path, include
from users.models import User
from solicitantes.views import ( 
    InfoPersonalRegistroView,  InteresView,
    #SoloAreaView,
    #SoloRolView,
)

urlpatterns = [
    #path('users/id/', InfoPersonalRegistroView.as_view()),
    path('users/', InfoPersonalRegistroView.as_view()),
    ##La linea se cambiará cuando se tenga ya el registro de los usuarios
    path('users/<int:usuario_id>/interes/', InteresView.as_view()),
    #path('users/<int:ususario_id>/area', SoloAreaView.as_view()),
    #path('users/<int:ususario_id>/rol', SoloRolView.as_view()),
] 