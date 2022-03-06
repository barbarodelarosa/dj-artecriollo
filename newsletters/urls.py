# from authy.models import PeopleList
from django.urls import path
from .views import NewslettersUnsubscribeView, newsletter_signup
app_name='newsletters'


urlpatterns = [
   	
    path('subscribe/', newsletter_signup, name='subscribe'),
    path('unsubscribe/', NewslettersUnsubscribeView.as_view(), name='unsubscribe'),
   
	
	


]


