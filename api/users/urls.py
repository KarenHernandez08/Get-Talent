from django import views
from django.urls import path
from users.views import UserSignupView
from users.views import VerifyEmail
from users.views import LoginAPIView
from users.views import Verificar
from users.views import ChangePasswordView
from users.views import PasswordResetEmailView
from users.views import PasswordResetView
from users.views import CodigoView
from users.views import LogoutView





urlpatterns = [
     
     path('signup/', UserSignupView.as_view(), name="signup"),
     
     path('email-verify/', VerifyEmail.as_view(), name="email-verify"), #se le coloca nombre porque es la liga que va a regresar
     
     path('login/', LoginAPIView.as_view(), name="login"),
     
     path('verify/', Verificar.as_view(), name="verificar"),
     
     path('change-password/', ChangePasswordView.as_view(), name='change-password'),  
     
     path('recovery/password-email/', PasswordResetEmailView.as_view(), name='recovery-password-email'),
     
     path('reset-password/', PasswordResetView.as_view(), name='reset-password'),

     path('recovery/codigo-acceso/', CodigoView.as_view()),
     
     path('logout/', LogoutView.as_view(), name="logout"),


]