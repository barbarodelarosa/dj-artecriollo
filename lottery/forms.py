"""
********************************************
*********** INFORMACION PENDIENDTE *********
********************************************

"""


from django.forms import Select
from shop.models import Product
from lottery.models import Lottery, Participant
from django import forms





class AddToParticipantLotteryForm(forms.ModelForm):
  
    amount = forms.FloatField(label="Precio de inscripción", initial=1)
    class Meta:
        model = Participant
        fields = ['amount']

    # def __init__(self, *args, **kwargs):
    #     auction_id = kwargs.pop('auction_id')
    #     auction = Auction.objects.get(id=auction_id)
    #     users_bid = UserBid.objects.filter(auction=auction).order_by('-bid_amount')
    #     bid_amount =  users_bid.first()
    #     porcent_bid_amount =  bid_amount.bid_amount * 0.01
    #     proposal = porcent_bid_amount + bid_amount

    #     super().__init__(*args, **kwargs)
    #     self.fields['bid_amount'].value = proposal


  
# from django.contrib.admin import widgets    

# class AddLotteryForm(forms.ModelForm):
    

#     product = forms.ModelChoiceField(queryset = Product.objects.none(),label="Producto a subastar", help_text="Selecciona el producto que desea poner en subasta", widget=Select(attrs={'class':'select2'}), required=False)

#     # date_finish = forms.DateTimeField()
#     date_finish = forms.SplitDateTimeField(label="Fecha de terminación", help_text="Agrege la fecha y hora de cierre para pujar", widget=widgets.AdminSplitDateTime())
#     price_init = forms.FloatField(label="Monto inicial", initial=0.00)
#     related_auction = forms.ModelMultipleChoiceField(label="Subastas relacionadas", queryset=Auction.objects.none(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    
  
#     class Meta:
#         model = Auction
#         fields = ['product','date_finish','price_init','related_auction']

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user')
#         super().__init__(*args, **kwargs)
        
        
#         self.fields['product'].queryset = Product.objects.filter(user=user)
#         self.fields['related_auction'].queryset = Auction.objects.all()
   
#         # self.fields['date_finish'].widget = widgets.AdminSplitDateTime