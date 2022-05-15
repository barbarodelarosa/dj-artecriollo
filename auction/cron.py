from auction.models import Auction, UserBid
from datetime import datetime
import random

def my_scheduled_job():
    auctions = Auction.objects.filter(aprobated=True, active=True, purchused=False)
    now = datetime.now().timestamp()
    for auction in auctions:
        if auction.date_finish.timestamp() <= now:
            winner = auction.userbid_set.all().order_by("-bid_amount").first()
            auction.purchused_by = winner.user
            auction.purchused=True
            auction.save()
            #Funcion enviar correos o notificaciones a los usuarios registrado y al admin
  
