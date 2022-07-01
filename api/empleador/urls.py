from django.urls import path, include

from empleador.views import InfoEmpleadorPostView

urlpatterns = [ 
    path('user_company/<int:usuario_id>/', InfoEmpleadorPostView.as_view()),
    
]