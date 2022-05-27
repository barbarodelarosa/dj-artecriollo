from datetime import datetime
from utils.enviar_emails import inscripcion_sorteo
from shop import enzona

from django.http import HttpResponse, HttpResponseRedirect
from lottery.forms import AddToParticipantLotteryForm
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import generic
from .models import Lottery, Participant, ParticipantPayment
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
    # form_class = CommentForm
    # def get_context_data(self, *args, **kwargs):
    #     context = super(LotteryDetailView, self).get_context_data(**kwargs)
    #     return context
        
    def post(self, request, *args, **kwargs):
        context = {}
        # context = super(LotteryDetailView, self).get_context_data(**kwargs)

        # form = self.form_class(request.POST)

        print("self.request.POST")
        print(self.request.POST)
        price = request.POST.get("price")
        lottery_id = request.POST.get("lottery_id")
        name = request.POST.get("title")
        description = request.POST.get("description")
        price = int(price)
        if price <= 0:

            lottery = Lottery.objects.get(id=lottery_id)

            try:
                participant_in_lottery = Participant.objects.get(user=self.request.user)

                if lottery == participant_in_lottery.lottery:
                    messages.error(request, message=f"Su cuenta ya esta registrada en el sorteo {lottery} por lo que no es posible volver a registrarse")

                    return HttpResponseRedirect(f'{request.build_absolute_uri()}')
            except:
                pass
            payment = ParticipantPayment.objects.create(
                user = self.request.user,
                amount = price,
                
            )

            participant = Participant.objects.create(
                user = self.request.user,
                amount = price,
                lottery = lottery,
                payment = payment
            )
            messages.info(request, message=f"Se ha registrado exitosamente en el sorteo {lottery} por un monto de {price} cup")
            inscripcion_sorteo(request, lottery_id, request.user.email)
            return HttpResponseRedirect(f'{request.build_absolute_uri()}')
        print("*********************price*****************")
        print(price)
        print(type(price))
        # plan = request.POST.get("plan")
    
        new_format_price = "{0:.2f}".format(price / 100)
        # new_format_price = f"{price}"
        
        

        items = []
        temp_item = {
        'name': name, #OJO ---> Los nombres no pueden tener caracteres especiales porque da error
        'description': description,
        'quantity': 1,
        'price': new_format_price,
        'tax': '0.00'
        }
        items.append(temp_item)
    
        amount = {
            "total": new_format_price,
            "details": {
            "shipping": "0.00",
            "tax": "0.00",
            "discount": "0.00",
            "tip": "0.00"
            }
        }
        
    
            
###################### BLOQUE DE CONSULTA A ENZONA #######################
        resp_enzona = enzona.post_payments(
            description=description,
            currency="CUP",
            amount=amount,
            items=items,
            cancel_url=f'{request.build_absolute_uri()}', #OK
            return_url=f'http://{request.get_host()}/lottery/{lottery_id}/confirm-pay-lottery/' #OK
            )
        print("resp_enzona.json()")
        print(resp_enzona.json())
        if resp_enzona.status_code == 200:
            
            resp_content = resp_enzona.json()
            links_resp = resp_content['links']
            url_confirm = links_resp[0]
            context['url_confirm'] = url_confirm
            request.session["user_id"]=request.user.pk
            request.session["lottery_id"]=lottery_id
            # request.session["plan"]=plan
            request.session["amount"]=resp_content['amount']['total']

            
            # guardar valores en session para desdupes de confirmado el pago utilizarlos y eliminarlos
            return redirect(to=url_confirm['href']) #Redirecciona a enzona para confirmar el pago
        else:
            print("resp_enzona.status_code")
            print(resp_enzona.status_code)
            print(resp_enzona.status_code)
                
        
            context['resp_enzona'] = resp_enzona.json()
        return HttpResponse('Pagado')

# Create your views here. 
# @login_required()





class ConfirmPayLotteryView(LoginRequiredMixin, generic.View): #Confirma el pago realizado por el usuario
    def get(self, request, *args, **kwargs):
        print("ESTOY AQUI********************************************")
        lottery_pay=None
        try:
        
            lottery_id=request.session["lottery_id"]
            # plan=request.session["plan"]
            # pago_plan = request.session['pago_plan']
            amount = request.session['amount']
            transaction_uuid = request.GET['transaction_uuid']
            user_uuid = request.GET['user_uuid']
            print("lottery")
            print(lottery_id)
            print("amount")
            print(amount)
            # print("plan_type")
            # print(plan_type)
        except:
            pass
        lottery = Lottery.objects.get(id=lottery_id)
        # lottery = Lottery.objects.get(id=1)

        # profile=Profile.objects.get(usuario=request.user)
        #  =Plan.objects.get(pk=1)
      
        #*******************************************************
        # Logica para agregar al usuario al sorteo#
        #*******************************************************
       
        payment = ParticipantPayment.objects.create(
            user = self.request.user,
            amount = amount,
            purchused = True,
            transaction_uuid = transaction_uuid,
            user_uuid = user_uuid
        )
        participant = Participant.objects.create(
            user = self.request.user,
            amount = amount,
            lottery = lottery,
            payment = payment
        )

    
        

        try:
            del request.session["lottery_id"]
            del request.session["amount"]
        except:
            pass
        # del request.session["transaction_uuid"]
        # del request.session['user_uuid']
        # del request.session['digital_product']
      

        messages.info(request, message=f"Se ha registrado en el sorteo {lottery} por un monto de {amount} cup")
        inscripcion_sorteo(request, lottery.id, request.user.email)
        # UserLibrary
        


        try:
            confirm = enzona.confirm_payment_orders(transaction_uuid)
            print("confirm")
            print(confirm)
        except:
            pass
        return redirect(lottery.get_absolute_url())

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