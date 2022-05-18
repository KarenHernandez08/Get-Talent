from django.urls import path, include
from infopersonal.views import InfoPersonalRegistroView, VideoSolicitanteView

urlpatterns = [
    path('patitos/', InfoPersonalRegistroView.as_view()),
    #path('users/<int:user_id>/', InfoPersonalRegistroView.as_view()),
    ##La linea se cambiará cuando se tenga ya el registro de los usuarios
    path('videosolicitante/', VideoSolicitanteView.as_view()),

]