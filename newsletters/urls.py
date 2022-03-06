# from authy.models import PeopleList
from django.urls import path
from .views import newsletter_signup, newslettes_unsubscribe

app_name='newsletters'


urlpatterns = [
   	
    path('subscribe/', newsletter_signup, name='subscribe'),
    path('unsubscribe/', newslettes_unsubscribe, name='unsubscribe'),
   
	
	


]


