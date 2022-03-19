

from auction.models import Auction, UserBid
from django import forms


class AddToUserBidForm(forms.ModelForm):
  
    bid_amount = forms.FloatField(label="Agregue monto a pujar", initial=1)
    class Meta:
        model = UserBid
        fields = ['bid_amount']

    # def __init__(self, *args, **kwargs):
    #     auction_id = kwargs.pop('auction_id')
    #     auction = Auction.objects.get(id=auction_id)
    #     users_bid = UserBid.objects.filter(auction=auction).order_by('-bid_amount')
    #     bid_amount =  users_bid.first()
    #     porcent_bid_amount =  bid_amount.bid_amount * 0.01
    #     proposal = porcent_bid_amount + bid_amount

    #     super().__init__(*args, **kwargs)
    #     self.fields['bid_amount'].value = proposal


  
  