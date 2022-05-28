import math
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from auction.models import Auction, UserBid
from datetime import datetime
import random

def my_scheduled_job():
    auctions = Auction.objects.filter(aprobated=True, active=True, purchused=False)
    now = datetime.now().timestamp()
    for auction in auctions:
        finish = auction.date_finish.timestamp()
        dias_restantes = math.floor((finish / (1000 * 60 * 60 * 24) - (now / (1000 * 60 * 60 * 24))) * 1000)
        horas_restantes = math.floor(((finish / (1000 * 60 * 60) - (now / (1000 * 60 * 60))) % 24) * 1000)
        if finish <= now:
            usersbid = auction.userbid_set.all().order_by("-bid_amount")
            winner = usersbid.first()
            auction.purchused_by = winner.user
            auction.purchused=True
            auction.save()
            #Funcion enviar correos o notificaciones a los usuarios registrado y al admin
            subject=f'Subasta del producto {auction.product}'
            
            from_email=settings.EMAIL_HOST_USER
            html_template='newsletters/email_templates/welcome.html'
            html_message_user=render_to_string(html_template)
            to_mail_user=[]
            for userbid in usersbid:
                to_mail_user.append(userbid.user.email)       
            message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
            message_user.content_subtype='html'
            message_user.send()

