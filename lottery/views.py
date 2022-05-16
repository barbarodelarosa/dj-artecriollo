from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect
from lottery.forms import AddToParticipantLotteryForm
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import generic
from .models import Lottery
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class LoteryListView(generic.ListView):
    # model = Auction
    template_name='lottery/index_lottery_list.html'
    paginate_by=10
    def get_queryset(self):
        return Lottery.objects.filter(aprobated=True, active=True).order_by('finished','-date_finish')


class LotteryDetailView(generic.DetailView):
    model = Lottery
    template_name='lottery/lottery_detail.html'

# Create your views here. 
# @login_required()
def addToParticipantLottery(request,pk):
    # user=request.user
    lottery = get_object_or_404(Lottery, pk=pk)
    user = request.user
    if request.method=="POST":
        form = AddToParticipantLotteryForm(request.POST)
        print(form)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.user=user
            participant.created_at=datetime.now()
            participant.amount=form.cleaned_data['amount']
            participant.lottery=lottery
            participant.save()
            
            messages.success(request, "Se ha subscrito exitosamente al sorteo por un monto de {}".format(participant.amount))
            
    next = request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
    return redirect(next)





# class CreateAuctionView(LoginRequiredMixin, generic.FormView):
#     template_name='lottery/create_lottery.html'
#     form_class=AddAuctionForm



#     def get_success_url(self):
#         return reverse("lottery:create-lottery")

#     def get_form_kwargs(self):
#         kwargs = super(CreateAuctionView, self).get_form_kwargs()
#         kwargs["user"] = self.request.user
#         print(self.request.user)
#         return kwargs

#     def form_invalid(self, form: AddAuctionForm) -> HttpResponse:
   
#         return super().form_invalid(form)


#     def form_valid(self, form):
#         related_lottery_list = []

#         related = form.cleaned_data.get('related_lottery')
#         for rel in related:
#             related_lottery_list.append(rel)


#         created = Lottery.objects.create(
#             user = self.request.user,
#             product = form.cleaned_data.get('product'),
#             created_at = form.cleaned_data.get('created_at'),
#             date_finish = form.cleaned_data.get('date_finish'),
#             price_init = form.cleaned_data.get('price_init'),
#             note = form.cleaned_data.get('note'),
          
#         )

#         created.related_lottery.set(related_lottery_list)
#         created.save()
#         messages.info(self.request,"Subasta creada exitosamente")
#         return super().form_valid(form)