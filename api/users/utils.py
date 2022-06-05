from django.core.mail import EmailMessage
import os
class Util: # el envio del email y es un metodo estatico
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['email_subject'], body=data['email_body'],to=[data['to_email']])
        
        email.send()
        
        


    
        