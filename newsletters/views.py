
import datetime
from utils.decorators import check_recaptcha
from utils.enviar_emails import nueva_orden
from django.conf import settings
from django.contrib import messages
from django.template import context
from django.urls import reverse
from newsletters.models import NewsletterUser
from newsletters.forms import NewsletterUserSigUpForm
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.views import generic
# Create your views here.

@check_recaptcha
def newsletter_signup(request):
    form = NewsletterUserSigUpForm(request.POST or None)


   
    # print(request.POST.get('email'))
    if form.is_valid():
        instance=form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            newsletter_user = NewsletterUser.objects.get(email=instance.email)
            if newsletter_user.subscribe == False:
                newsletter_user.subscribe = True
                newsletter_user.resubscribe_date = datetime.datetime.now()
                newsletter_user.save()
                #Correo electronico
                subject="Inscripción a boletín de ArteCiollo"
                subject_admin="Nueva Inscripción a boletín de ArteCiollo"
                email_admin=settings.EMAIL_HOST_USER
                from_email=email_admin
                to_mail_user=[instance.email]
                to_mail_admin=[from_email]

                html_template='newsletters/email_templates/welcome.html'
                html_message_user=render_to_string(html_template)
                html_message_admin=f'Nuevo usuario registrado al boletin email:{to_mail_user}'
                
                message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
                message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)
                
                message_user.content_subtype='html'
                message_user.send()
                message_admin.send()
                


                messages.success(request, 'Hemos enviado un correo electrónico a su cuenta confirmando su inscripción :)')
            else:
                messages.warning(request, 'El correo ya existe. Por favor agregue otro correo que usted utilice')
        else:
            instance.save()
            #Correo electronico
            subject="Inscripción a boletín de ArteCiollo"
            subject_admin="Nueva Inscripción a boletín de ArteCiollo"

            email_admin=settings.EMAIL_HOST_USER
            from_email=email_admin
            to_mail_user=[instance.email]
            to_mail_admin=[from_email]

            html_template='newsletters/email_templates/welcome.html'
            html_message_user=render_to_string(html_template)
            html_message_admin=f'Nuevo usuario registrado al boletin email:{to_mail_user}'

            message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
            message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)

           
                          
            message_user.content_subtype='html'
            message_user.send()
            message_admin.send()
            messages.success(request, 'Hemos enviado un correo electrónico a su cuenta confirmando su inscripción')
                


    next = request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual

    return redirect(next)


    


class NewslettersUnsubscribeView(generic.FormView):
    form_class = NewsletterUserSigUpForm
    template_name= 'newsletters/unsubscribe.html'

    def get_success_url(self):
        return reverse("home")

    def form_valid(self, form):
        next = self.request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual

       
        email = form.cleaned_data.get('email')

        if NewsletterUser.objects.filter(email=email).exists():
            newletters_user = NewsletterUser.objects.get(email=email)
            if newletters_user.subscribe == False:
                messages.warning(self.request, "El correo no está subscrito a nuestro servico")
                return redirect(next)

            newletters_user.subscribe = False
            newletters_user.unsubscribe_date = datetime.datetime.now()
            newletters_user.save()
            
            subject="Eliminación de Subscripción boletín de ArteCiollo"
            subject_admin="Eliminación de Subscripción a boletín de ArteCiollo"

            email_admin=settings.EMAIL_HOST_USER
            from_email=email_admin
            to_mail_user=[email]
            to_mail_admin=[from_email]

            html_template='newsletters/email_templates/unsubscribe.html'
            html_message_user=render_to_string(html_template)
            html_message_admin=f'Usuario eliminado de la subscripción al boletín:{to_mail_user}'

            message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
            message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)

           
                          
            message_user.content_subtype='html'
            message_user.send()
            message_admin.send()
            messages.success(self.request, "El correo ha sido eliminado")
        else:

            
            subject_admin="Alerta de Intento de Eliminación de Subscripción a boletín de ArteCiollo"

            email_admin=settings.EMAIL_HOST_USER
            from_email=email_admin
            to_mail_user=[email]
            to_mail_admin=[from_email]

            html_template='newsletters/email_templates/unsubscribe.html'
            
            html_message_admin=f'Intento de eliminacion de subscripción del correo {to_mail_user} al boletín'

           
            message_admin=EmailMessage(subject_admin,html_message_admin,from_email, to_mail_admin)

            message_admin.send()

            messages.warning(self.request, "El correo no ha sido encontrado")
            return redirect(next)


        #Enviar correo de notificacion aqui tambien
        # full_message = f"""
        #     Mensaje recibido de {name}, {email}
        #     ___________________________________

        #     {message}
        #     """

        # send_mail(
        #     subject="Mensaje recibido por contact form",
        #     message=full_message,
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[settings.NOTIFY_EMAIL]
        # )
        return super(NewslettersUnsubscribeView, self).form_valid(form)