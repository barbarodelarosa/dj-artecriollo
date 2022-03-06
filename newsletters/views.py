import email
from django.conf import settings
from django.contrib import messages
from django.template import context
from newsletters.models import NewsletterUser
from newsletters.forms import NewsletterUserSigUpForm
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage

# Create your views here.

def newsletter_signup(request):
    form = NewsletterUserSigUpForm(request.POST or None)
   
    # print(request.POST.get('email'))
    if form.is_valid():
        instance=form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.info(request, 'El correo ya existe.')
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



def newslettes_unsubscribe(request):
    form = NewsletterUserSigUpForm(request.POST or None)
   
    print("TODO BIEN")
    print(form)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            newletters_user = NewsletterUser.objects.filter(email=instance.email)
            newletters_user.subscribe = False
            newletters_user.update()
            messages.success(request, "El correo ha sido eliminado")
        else:
            messages.warning(request, "El correo no ha sido encontrado")
    
    return render(request, template_name='newsletters/email_templates/unsubscribe.html')
    