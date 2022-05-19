from django import views
from django.urls import path
from users.views import UserSignupView
from users.views import VerifyEmail
from users.views import LoginAPIView
from users.views import Verificar
from users.views import RequestPasswordResetEmail
from users.views import PasswordTokenCheckAPI
from users.views import SetNewPasswordAPIView






urlpatterns = [
    path('signup/', UserSignupView.as_view(), name="signup"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"), #se le coloca nombre porque es la liga que va a regresar
    path('login/', LoginAPIView.as_view(), name="login"),
    path('verify/', Verificar.as_view(), name="verificar"),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')
]
