 
from django.urls import path
from . import views

urlpatterns = [
    path('', views.InicioAPIView.as_view(),),
]