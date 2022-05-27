from datetime import datetime
from utils.enviar_emails import inscripcion_subasta

from django.http import HttpResponse, HttpResponseRedirect
from auction.forms import AddAuctionForm, AddToUserBidForm
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import generic
from .models import Auction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class ActionProductsListView(generic.ListView):
    # model = Auction
    template_name='auction/index_auction_list.html'
    paginate_by=10
    def get_queryset(self):
        return Auction.objects.filter(aprobated=True, active=True).order_by('purchused','-date_finish')


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
            inscripcion_subasta(request, pk, request.user.email)
            
    next = request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
    return redirect(next)





class CreateAuctionView(LoginRequiredMixin, generic.FormView):
    template_name='auction/create_auction.html'
    form_class=AddAuctionForm



    def get_success_url(self):
        return reverse("auction:create-auction")

    def get_form_kwargs(self):
        kwargs = super(CreateAuctionView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        print(self.request.user)
        return kwargs

    def form_invalid(self, form: AddAuctionForm) -> HttpResponse:
   
        return super().form_invalid(form)


    def form_valid(self, form):
        related_auction_list = []

        related = form.cleaned_data.get('related_auction')
        for rel in related:
            related_auction_list.append(rel)


        created = Auction.objects.create(
            user = self.request.user,
            product = form.cleaned_data.get('product'),
            created_at = form.cleaned_data.get('created_at'),
            date_finish = form.cleaned_data.get('date_finish'),
            price_init = form.cleaned_data.get('price_init'),
            note = form.cleaned_data.get('note'),
          
        )

        created.related_auction.set(related_auction_list)
        created.save()
        messages.info(self.request,"Subasta creada exitosamente")
        return super().form_valid(form)