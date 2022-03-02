from typing import OrderedDict
from unicodedata import category

from django.http import request
from shop.enzona import payment_orders
from django import shortcuts
from django.forms import forms
from django.shortcuts import render, reverse

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
# Create your views here.


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'orders': Order.objects.filter(user=self.request.user, ordered=True)
        })
        return context



class HomeView(generic.TemplateView):
   
    template_name = 'new-theme/index.html'
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context.update({
                'orders': Order.objects.filter(user=self.request.user, ordered=True),
                'category_list': Category.objects.all(),
                'nav_active':'active',
            })
        else:
            context.update({
                'orders': [],
                'category_list': Category.objects.all(),
                'nav_active':'active',
            })
        return context




class ContactView(generic.FormView):
    form_class = ContactForm
    template_name= 'new-theme/contact.html'

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
    template_name = 'new-theme/search_results.html'
    


    def get_queryset(self):
        query = self.request.GET.get('q', '')
        query_category = self.request.GET.get('q_category', '')
        # if not query:
        #     query = ""
        print('query_category')
        print(query_category)
        print('query_categorysss')
        if query_category == '0':
            object_list = Product.objects.filter(Q(title__contains=query)|Q(description__contains=query)).order_by(
                "updated",
                "created",
                "title",
            )
        else:       
            object_list = Product.objects.filter(
            Q(category=query_category)).filter(Q(title__contains=query)|Q(description__contains=query)).order_by(
                "updated",
                "created",
                "title",
            )
        # object_list.filter(Q(title__contains=query)|Q(description__contains=query))
       

        paginator = Paginator(object_list, 1)
        # object_list = object.page(page).object_list
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj
        
    
    def get_context_data(self, **kwargs):

        context = super(SearchResultsView, self).get_context_data(**kwargs)
        parametros = self.request.GET.copy() # Es una copia del GET

        context['parametros'] = parametros
    
        if (parametros.get('page') != None):
            del parametros['page']
        else:
            del parametros
        return context


    
    