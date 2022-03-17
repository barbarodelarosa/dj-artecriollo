from django.shortcuts import render
from django.views import generic
from .models import Auction

class ActionProductsListView(generic.ListView):
    model = Auction
    template_name='auction/index_auction_list.html'

class ActionProductsDetailView(generic.DetailView):
    model = Auction
    template_name='auction/auction_detail.html'

# Create your views here.
