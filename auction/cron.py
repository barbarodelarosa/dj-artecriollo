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
