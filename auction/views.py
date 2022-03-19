from datetime import datetime
from auction.forms import AddToUserBidForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Auction
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class ActionProductsListView(generic.ListView):
    model = Auction
    template_name='auction/index_auction_list.html'
    paginate_by=2

class ActionProductsDetailView(generic.DetailView):
    model = Auction
    template_name='auction/auction_detail.html'

# Create your views here.
# @login_required()
def addToUserBid(request,pk):
    # user=request.user
    auction = get_object_or_404(Auction, pk=pk)
    user = request.user
    if request.method=="POST":
        form = AddToUserBidForm(request.POST)
        print(form)
        if form.is_valid():
            user_bid = form.save(commit=False)
            user_bid.user=user
            user_bid.created_at=datetime.now()
            user_bid.bid_amount=form.cleaned_data['bid_amount']
            user_bid.auction=auction
            user_bid.save()
            
            messages.info(request, "Usted ha pujado por un monto de {}".format(user_bid.bid_amount))
            
    next = request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
    return redirect(next)