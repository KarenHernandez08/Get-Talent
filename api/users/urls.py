from django import views
from django.urls import path
from users.views import UserSignupView
from users.views import VerifyEmail
from users.views import LoginAPIView



urlpatterns = [
    path('signup/', UserSignupView.as_view(), name="signup"),
    #path('registers/', UserListView.as_view()),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"), #se le coloca nombre porque es la liga que va a regresar
    path('login/', LoginAPIView.as_view(), name="login"),
]