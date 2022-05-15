from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from lottery.models import Lottery, Participant
from datetime import datetime
import random

def my_scheduled_job():
    lotteries = Lottery.objects.filter(aprobated=True, active=True, finished=False)
    now = datetime.now().timestamp()
    for lottery in lotteries:
        if lottery.date_finish.timestamp() <= now:
            total_winners=lottery.total_winners
            participants = Participant.objects.filter(lottery=lottery)
            winners = random.sample(list(participants), total_winners)
            
            for winner in winners:
                participant = winner
                participant.winner = True
                participant.save()
                lottery.winners.add(participant.user)
           
            lottery.finished = True
            lottery.save()

            subject=f'Sorteo {lottery.product}'
            
            from_email=settings.EMAIL_HOST_USER
            html_template='newsletters/email_templates/welcome.html'
            html_message_user=render_to_string(html_template)
            to_mail_user=[]
            for parti in participants:
                to_mail_user.append(parti.user.email)

            message_user=EmailMessage(subject,html_message_user,from_email, to_mail_user)
            message_user.content_subtype='html'
            message_user.send()
