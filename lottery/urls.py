from django.urls import path

from . import views

app_name='lottery'
urlpatterns = [
    path('', views.LoteryListView.as_view(), name='lottery-index'),
    # path('create-auction/', views.CreateAuctionView.as_view(), name='create-auction'), 
    path('<pk>/', views.LotteryDetailView.as_view(), name='lottery-detail'), 
    path('<pk>/add-participant-lottery/', views.addToParticipantLottery, name='add-participant-lottery'), 
    path('<pk>/confirm-pay-lottery/', views.ConfirmPayLotteryView.as_view(), name='confirm-pay-lottery'), 
    # path('pay-lottery/', views.lotteryPay, name='pay-lottery'), 
  
]