from lottery.models import Lottery, Participant
from datetime import datetime
import random

def my_scheduled_job():
    lotteries = Lottery.objects.filter(finished=False)
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
