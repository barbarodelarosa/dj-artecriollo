from django.urls import path

from . import views

app_name='utils'
urlpatterns = [
       path('maps', views.SomeLocationModelView.as_view(), name='maps'),





]