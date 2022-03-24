from django.urls import path

from . import views

app_name='auction'
urlpatterns = [
    path('', views.ActionProductsListView.as_view(), name='auction-index'),
    path('create-auction/', views.CreateAuctionView.as_view(), name='create-auction'), 
    path('<pk>/', views.ActionProductsDetailView.as_view(), name='auction-detail'), 
    path('<pk>/user-bid-amount/', views.addToUserBid, name='user-bid-amount'), 
  
]