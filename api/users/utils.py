from django.core.mail import EmailMessage


class Util: # el envio del email y es un metodo estatico
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['email_subject'], body=data['email_body'],to=[data['to_email']])
        
        email.send()
        
        '''
        email_subject: asunto
        email_body: lo que se le va a enviar
        to: el correo al que se le va a enviar
        '''