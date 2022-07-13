
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import permissions

from solicitantes.models import *
from vacantes.models import *
from .serializers import PostulacionesSerializer
#from postulaciones.renderers import PostulacionesRenderer




# Create your views here.

class PostulacionesView(generics.GenericAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    #renderer_classes=(PostulacionesRenderer,)
    serializer_class = PostulacionesSerializer
     
    def post(self, request, vacante_id):  
        data = request.data
        solicitante_instance = request.user
        id_user = solicitante_instance.id
        id_usuario =data.get('user_id')
        es_empleador= solicitante_instance.is_empleador
        
        informacion_personal = bool(InfoPesonalModel.objects.filter(user_id= id_user))
        print(informacion_personal)
        informacion_academica = bool(InfoAcademicaModel.objects.filter (user_id = id_user))
        video_solicitante =bool(VideoSolicitanteModel.objects.filter (user_id = id_user))
        intereses = bool(InteresModel.objects.filter(user_id = id_user))
        vacante=bool(VacantesModel.objects.filter(vacante_id= vacante_id))
         
        try:
            if vacante == None:
                    return Response('la vacante no existe', status = status.HTTP_400_BAD_REQUEST)
            if es_empleador == True:    
                    return Response('No tienes autorización', status=status.HTTP_401_UNAUTHORIZED)
                
                
            elif es_empleador == False:
                if informacion_personal == False:
                    return Response('No ha colocado su información personal', status = status.HTTP_400_BAD_REQUEST)
                if informacion_academica == False:
                    return Response('No ha colocado información academica', status = status.HTTP_400_BAD_REQUEST)
                if video_solicitante == False:
                    return Response('El video es importante, subir link de su video', status = status.HTTP_400_BAD_REQUEST)
                #if intereses == False:
                    #return Response('El video es importante, subir link de su video', status = status.HTTP_400_BAD_REQUEST) 
                if id_usuario == id_user:           
                        
                    serializer = PostulacionesSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True) 
                    serializer.save()     
                    return Response('Postulación Autorizada', status=status.HTTP_201_CREATED)
                else:
                    return Response('El usuario es incorrecto', status = status.HTTP_400_BAD_REQUEST)        
                    
        except:
            return Response('Revise nuevamente', status=status.HTTP_400_BAD_REQUEST)

        