from django import views
from django.urls import path, include

from users.views import UserSignupView
from users.views import VerifyEmail
urlpatterns = [
    path('signup/', UserSignupView.as_view(), name="signup"),
    #path('registers/', UserListView.as_view()),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
]