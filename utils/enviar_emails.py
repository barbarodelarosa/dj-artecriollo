from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage


        
def nueva_orden(request, order,tipo_producto):
        subject=f"ORDEN DE COMPRA #{order.id} - ARTECRIOLLO"
        subject_admin=f"NUEVA ORDEN DE COMPRA ({order.id})"
        email_admin=settings.EMAIL_HOST_USER
        from_email=email_admin
        to_mail_user=[request.user.email]
        to_mail_admin=[from_email]
        if tipo_producto == "PRODUCTO DIGITAL":
                html_template='emails/shop/nueva_orden_digital.html'
                html_message_user=render_to_string(html_template,{'product':order, 'usuario_email':request.user.username})
                print("HASTA AQUI TODO BIEN CON EL CORRO DEL PRODUCTO DIGITAL")
                html_message_admin=f'TIPO DE PRODUCTO:{tipo_producto} Nueva orden de compra de producto ({order}) por el usuario {to_mail_user}'
        else:
                html_template='emails/shop/nueva_orden.html'
                html_message_user=render_to_string(html_template,{'order':order, 'usuario_email':request.user.username})
                html_message_admin=f'TIPO DE PRODUCTO:{tipo_producto} Nueva orden de compra ({order.id}) por el usuario {to_mail_user}'

        
        message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
        message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)
        
        message_user.content_subtype='html'
        print("ANTES DE ENVIAR")
        message_user.send()
        print("DESPUES DE ENVIAR")
        message_admin.send()        
        messages.success(request, 'Hemos enviado un correo electrónico a su cuenta confirmando su pedido :)')


################   SUBASTA  ################

def inscripcion_subasta(request, numero_subasta, email_user):
        subject=f"INSCRIPCION A SUBASTA #{numero_subasta} - ARTECRIOLLO"
        subject_admin=f"NUEVA INSCRIPCION A SUBASTA ({numero_subasta})"
        email_admin=settings.EMAIL_HOST_USER
        from_email=email_admin
        to_mail_user=[email_user]
        to_mail_admin=[from_email]

        html_template='emails/subasta/inscripcion_subasta.html'
        html_message_user=render_to_string(html_template,{'usuario_email':request.user.username})
        html_message_admin=f'Nueva orden de compra ({numero_subasta}) por el usuario {to_mail_user}'
        
        message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
        message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)
        
        message_user.content_subtype='html'
        message_user.send()
        message_admin.send()        
        messages.success(request, f'Hemos enviado un correo de confirmación de su inscripcion a la subasta #{numero_subasta}')


def cierre_subasta(numero_subasta, email_user):
        subject=f"SUBASTA #{numero_subasta} CERRADA - ARTECRIOLLO"
        subject_admin=f"SUBASTA #{numero_subasta} CERRADA"
        email_admin=settings.EMAIL_HOST_USER
        from_email=email_admin
        to_mail_user=[email_user]
        to_mail_admin=[from_email]

        html_template='emails/subasta/cierre_subasta.html'
        html_message_user=render_to_string(html_template,{'prueba':'PRUEBA PERFECTA'})
        html_message_admin=f'Nueva orden de compra ({numero_subasta}) por el usuario {to_mail_user}'
        
        message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
        message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)
        
        message_user.content_subtype='html'
        message_user.send()
        message_admin.send()        


def pre_cierre_subasta(numero_subasta, email_user):
        subject=f"PRE-CIERRE DE SUBASTA #{numero_subasta} - ARTECRIOLLO"
        subject_admin=f"PRE-CIERRE DE SUBASTA #{numero_subasta}"
        email_admin=settings.EMAIL_HOST_USER
        from_email=email_admin
        to_mail_user=[email_user]
        to_mail_admin=[from_email]

        html_template='emails/subasta/pre_cierre_subasta.html'
        html_message_user=render_to_string(html_template,{'prueba':'PRUEBA PERFECTA'})
        html_message_admin=f'Nueva orden de compra ({numero_subasta}) por el usuario {to_mail_user}'
        
        message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
        message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)
        
        message_user.content_subtype='html'
        message_user.send()
        message_admin.send()   

def nueva_puja_subasta(numero_subasta, email_user):
        subject=f"NUEVA PUJA EN SUBASTA #{numero_subasta} - ARTECRIOLLO"
        subject_admin=f"NUEVA PUJA EN SUBASTA #{numero_subasta}"
        email_admin=settings.EMAIL_HOST_USER
        from_email=email_admin
        to_mail_user=[email_user]
        to_mail_admin=[from_email]

        html_template='emails/subasta/nueva_puja_subasta.html'
        html_message_user=render_to_string(html_template,{'prueba':'PRUEBA PERFECTA'})
        html_message_admin=f'Nueva orden de compra ({numero_subasta}) por el usuario {to_mail_user}'
        
        message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
        message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)
        
        message_user.content_subtype='html'
        message_user.send()
        message_admin.send()   



#############  SORTEO  ####################

def inscripcion_sorteo(request, numero_sorteo, email_user):
  
        subject=f"INSCRIPCION A SORTEO #{numero_sorteo} - ARTECRIOLLO"
        subject_admin=f"NUEVA INSCRIPCION A SORTEO ({numero_sorteo})"
        email_admin=settings.EMAIL_HOST_USER
        from_email=email_admin
        to_mail_user=[email_user]
        to_mail_admin=[from_email]

        html_template='emails/sorteo/inscripcion_sorteo.html'
        html_message_user=render_to_string(html_template)
        html_message_admin=f'Nueva orden de compra ({numero_sorteo}) por el usuario {to_mail_user}'
        
        message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
        message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)
        
        message_user.content_subtype='html'
        message_user.send()
        message_admin.send()        
        messages.success(request, f'Hemos enviado un correo de confirmación de su participación en el sorteo #{numero_sorteo}')

def pre_cierre_sorteo(numero_sorteo, email_user):
        subject=f"PRE CIERRE DE SORTEO #{numero_sorteo} - ARTECRIOLLO"
        subject_admin=f"PRE CIERRE DE SORTEO ({numero_sorteo})"
        email_admin=settings.EMAIL_HOST_USER
        from_email=email_admin
        to_mail_user=[email_user]
        to_mail_admin=[from_email]

        html_template='emails/sorteo/pre_cierre_sorteo.html'
        html_message_user=render_to_string(html_template,{'prueba':'PRUEBA PERFECTA'})
        html_message_admin=f'Nueva orden de compra ({numero_sorteo}) por el usuario {to_mail_user}'
        
        message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
        message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)
        
        message_user.content_subtype='html'
        message_user.send()
        message_admin.send()        

def cierre_sorteo(numero_sorteo, email_user):
        subject=f"CIERRE DE SORTEO #{numero_sorteo} - ARTECRIOLLO"
        subject_admin=f"CIERRE DE SORTEO ({numero_sorteo})"
        email_admin=settings.EMAIL_HOST_USER
        from_email=email_admin
        to_mail_user=[email_user]
        to_mail_admin=[from_email]

        html_template='emails/sorteo/cierre_sorteo.html'
        html_message_user=render_to_string(html_template,{'prueba':'PRUEBA PERFECTA'})
        html_message_admin=f'Nueva orden de compra ({numero_sorteo}) por el usuario {to_mail_user}'
        
        message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
        message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)
        
        message_user.content_subtype='html'
        message_user.send()
        message_admin.send() 

def nueva_participacion_sorteo(numero_sorteo, email_user):
        subject=f"CIERRE DE SORTEO #{numero_sorteo} - ARTECRIOLLO"
        subject_admin=f"CIERRE DE SORTEO ({numero_sorteo})"
        email_admin=settings.EMAIL_HOST_USER
        from_email=email_admin
        to_mail_user=[email_user]
        to_mail_admin=[from_email]

        html_template='emails/sorteo/nueva_participacion_sorteo.html'
        html_message_user=render_to_string(html_template,{'prueba':'PRUEBA PERFECTA'})
        html_message_admin=f'Nueva orden de compra ({numero_sorteo}) por el usuario {to_mail_user}'
        
        message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
        message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)
        
        message_user.content_subtype='html'
        message_user.send()
        message_admin.send()


