from django.urls import path, include
from users.models import User
from solicitantes.views import (
    InfoPersonalRegistroView,
    VideoSolicitanteView,
)

urlpatterns = [
    path('users/<int:usuario_id>/', InfoPersonalRegistroView.as_view()),
    path('videosolicitante/', VideoSolicitanteView.as_view()),
    #path('videosolicitante/<int:usuario_id>/', VideoSolicitanteView.as_view()),
    ##La linea se cambiará cuando se tenga ya el registro de los usuarios
]