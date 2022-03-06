import email
import datetime
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
                messages.success(request, 'Hemos enviado un correo electrónico a su correo que ya existia')
                #Correo electronico
                subject="Correo de prueba"
                from_email=settings.EMAIL_HOST_USER
                to_mail=[instance.email]

                html_template='newsletters/email_templates/welcome.html'
                html_message=render_to_string(html_template)
                message=EmailMessage(subject,html_message,from_email, to_mail)
                message.content_subtype='html'
                message.send()
            else:
                messages.warning(request, 'El correo ya existe. Por favor agregue otro correo que usted utilice')
        else:
            instance.save()
            messages.success(request, 'Hemos enviado un correo electrónico a su correo')
            #Correo electronico
            subject="Correo de prueba"
            from_email=settings.EMAIL_HOST_USER
            to_mail=[instance.email]

            html_template='newsletters/email_templates/welcome.html'
            html_message=render_to_string(html_template)
            message=EmailMessage(subject,html_message,from_email, to_mail)
            message.content_subtype='html'
            message.send()


    next = request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual

    return redirect(next)


    


class NewslettersUnsubscribeView(generic.FormView):
    form_class = NewsletterUserSigUpForm
    template_name= 'newsletters/email_templates/unsubscribe.html'

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
            messages.success(self.request, "El correo ha sido eliminado")
        else:
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