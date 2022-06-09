from lottery.models import Lottery, Participant
from affiliate.models import Shortener
from logging import FileHandler
import os
from utils.views import change_info
# import requests
from core.models import Page

from django.http import Http404, HttpResponse, HttpResponseRedirect, request
from shop.enzona import payment_orders
from django import shortcuts
from django.forms import forms
from django.shortcuts import redirect, render, reverse

from django.core.mail import send_mail
from django.contrib import messages
# from artecriollo import settings
from django.conf import settings
from django.views import generic
from .forms import ContactForm
from shop import enzona
from shop.models import Category, Order, Product
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from profile.models import Profile, UserLibrary
from auction.models import Auction, UserBid
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required





from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_user_notification
import json


# Create your views here.


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        # try:
        ref_profile = self.request.session.get('ref_profile')
        registered_user = User.objects.get(id=self.request.user.id)
        registered_profile = Profile.objects.get(user=registered_user)
        # profile = Profile.objects.get(user=self.request.user)
        if registered_profile.recommended_by is None:
            if ref_profile is not None:
                print("ref_profile",ref_profile)
                recommended_by_profile = Profile.objects.get(user_id=ref_profile)
                registered_profile = Profile.objects.filter(user=registered_user).update(recommended_by=recommended_by_profile)

                
                print("recommended_by_profile:",recommended_by_profile)
                # registered_profile.recommended_by = recommended_by_profile
                print("Recomended:",registered_profile)
                # registered_profile.save()
        # except:
            # print("NO HAY NADA")
            # pass
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'orders': Order.objects.filter(user=self.request.user, ordered=True),
            'recommended': Profile.objects.filter(recommended_by=self.request.user),
            'recommended_order': Order.objects.filter(user_recommended=self.request.user),
            'library': UserLibrary.objects.get(user=self.request.user),
            'participations': Participant.objects.filter(user=self.request.user).order_by('-created_at'),
            'userbids': UserBid.objects.filter(user=self.request.user).order_by('-created_at')
        })
        return context


from django.contrib import messages

class HomeView(generic.TemplateView):
   
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        messages.success(request, 'ANTESSSS')
        payload = {"head": "Welcome!", "body": "Hello World"}
        user = get_object_or_404(User, id=request.user.id)
        send_user_notification(user=user, payload=payload, ttl=1000)    
        messages.success(request, 'DESPUESSS')
        change_info(self.request)
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context.update({
                'orders': Order.objects.filter(user=self.request.user, ordered=True),
                'category_list': Category.objects.filter(active=True)[:6],
                'new_products': Product.objects.filter(aprobated=True).filter(for_auction=False).filter(active=True).order_by('created','updated')[:6],
                'top_selling': Product.objects.filter(aprobated=True).filter(for_auction=False).filter(active=True, selling=True).order_by('created', 'selling_date', 'updated')[:6],
                'new_auction': Auction.objects.filter(aprobated=True, active=True).order_by('purchused','-date_finish')[:6],
                'nav_active':'active',
            })
        else:
            context.update({
                'orders': [],
                'category_list': Category.objects.filter(active=True)[:3],
                'new_products': Product.objects.filter(aprobated=True).filter(for_auction=False).filter(active=True).order_by('created','updated')[:6],
                'top_selling': Product.objects.filter(aprobated=True).filter(for_auction=False).filter(active=True, selling=True).order_by('created', 'selling_date', 'updated')[:6],
                'new_auction': Auction.objects.filter(aprobated=True, active=True).order_by('purchused','-date_finish')[:6],
                'nav_active':'active',
            })
        return context




class ContactView(generic.FormView):
    form_class = ContactForm
    template_name= 'pages/contact.html'

    def get_success_url(self):
        return reverse("contact")

    def form_valid(self, form):
        messages.info(
            self.request, "Hemos recibido tu mensaje"
        )
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')
 
        full_message = f"""
            Mensaje recibido de {name}, {email}
            ___________________________________

            {message}
            """

        send_mail(
            subject="Mensaje recibido por contact form",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]
        )
        return super(ContactView, self).form_valid(form)



class SearchResultsView(generic.ListView):
    model = Product
    template_name = 'search_results.html'
    


    def get_queryset(self):
    
        query = self.request.GET.get('q', '')
        query_category = self.request.GET.get('q_category', '')
        # if not query:
        #     query = ""
       
        # if query_category == '0':
        #     object_list = Product.objects.filter(Q(title__contains=query)|Q(description__contains=query)).order_by(
        #         "updated",
        #         "created",
        #         "title",
        #     )
        # else:       
        #     object_list = Product.objects.filter(
        #     Q(category=query_category)).filter(Q(title__contains=query)|Q(description__contains=query)).order_by(
        #         "updated",
        #         "created",
        #         "title",
        #     )

        object_list = self.results_query_object_list(query, query_category)
        # object_list.filter(Q(title__contains=query)|Q(description__contains=query))
        # self.count_result_object_list(object_list)
        paginator = Paginator(object_list, 2)
        # object_list = object.page(page).object_list
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj
        
    
    def get_context_data(self, **kwargs):
        query = self.request.GET.get('q', '')
        query_category = self.request.GET.get('q_category', '')

        context = super(SearchResultsView, self).get_context_data(**kwargs)
        parametros = self.request.GET.copy() # Es una copia del GET

        context['parametros'] = parametros
        context['count_result_query'] = self.results_query_object_list(query, query_category).count()
      

    
        if (parametros.get('page') != None):
            del parametros['page']
        else:
            del parametros
        return context
    
    def results_query_object_list(self, query, query_category):
        if query_category == '0':
            object_list = Product.objects.filter(for_auction=False).filter(Q(title__contains=query)|Q(description__contains=query)).order_by(
                "updated",
                "created",
                "title",
            )
        else:       
            object_list = Product.objects.filter(for_auction=False).filter(
            Q(category=query_category)).filter(Q(title__contains=query)|Q(description__contains=query)).order_by(
                "updated",
                "created",
                "title",
            )
        
        
        return object_list


    
class AboutView(generic.TemplateView):
    template_name = 'pages/about.html'

    
class PrivacyView(generic.TemplateView):
    template_name = 'pages/privacy.html'


class TermsView(generic.TemplateView):
    template_name = 'pages/terms.html'


class HelpView(generic.TemplateView):
    template_name = 'pages/help.html'


class PageDetailView(generic.DetailView):
    model = Page
    template_name="pages/page_detail.html"


@login_required()
def downloadFile(request):
    # user=request.user
    # auction = get_object_or_404(Auction, pk=pk)
    # user = request.user
    if request.method=="POST":
       #probar que sea valido el formulario para descarga

        # full_path = os.path.join(settings.MEDIA_ROOT, 'bootstrap-5.1.3-examples.zip') #OKKK
        full_path = os.path.join(settings.MEDIA_ROOT, 'user_barbaro/product_hero.jpg')
        content = open(full_path, "rb")
        response = HttpResponse(content.read(), content_type="application/adminupload")
        response['Content-Disposition']='inline;filename='+os.path.basename(full_path)

        return response
            
    next = request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
    return redirect(next)

from django_downloadview import HTTPDownloadView

class GithubAvatarDownloadView(HTTPDownloadView):
    def get_url(self):
        return "http://127.0.0.1:8000/bootstrap-5.1.3-examples.zip"




def redirect_url_view(request, shortened_part):

    try:
        shortener = Shortener.objects.get(short_url=shortened_part)

        shortener.times_followed += 1        

        shortener.save()
        # new_url = request.build_absolute_uri('/') + shortened_object.short_url
        print("request.get_host('/')")
        print(request.build_absolute_uri('/'))
        print(request.get_host())
        next_url = request.build_absolute_uri('/') + shortener.long_url
        print(next_url)
        
        return HttpResponseRedirect(next_url)
        
    except:
        raise Http404('Lo sentimos, enlace roto :(')



def pag_404_not_found(request, exception):
    return render(request, '404.html')

def pag_500_error_server(request):
    return render(request, '500.html')


def pag_403_forbidden(request, exception):
    return render(request, '403.html')


