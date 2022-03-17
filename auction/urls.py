from django.urls import path

from . import views

app_name='auction'
urlpatterns = [
    path('', views.ActionProductsListView.as_view(), name='auction-index'),
    path('<pk>/', views.ActionProductsDetailView.as_view(), name='auction-detail'), 
  
]