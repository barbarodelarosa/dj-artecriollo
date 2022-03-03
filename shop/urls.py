from django.urls import path

from . import views

app_name='shop'
urlpatterns = [
    path('cart', views.CartView.as_view(), name='summary'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    # path('category/<category>/', views.CategoryDeatilView.as_view(), name='category-detatil'),
    
    path('whishlist/', views.WhishlistView.as_view(), name='whishlist'),
    
    path('<slug>/', views.ProductListView.as_view(), name='product-list'),
    # path('<slug>', views.CategoryDeatilView.as_view(), name='category-detail'),
    path('<category>/<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('increase-quantity/<pk>/', views.IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<pk>/', views.DecreaseQuantityView.as_view(), name='decrease-quantity'),
    path('remove-from-cart/<pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('payment-enzona/', views.ConfirmEnzonaPaymentView.as_view(), name='payment-enzona'),
    path('confirm-order/', views.ConfirmOrderView.as_view(), name='confirm-order'),
    path('thankyou/', views.ThankYouView.as_view(), name='thankyou'),
    path('orders/<pk>', views.OrderDetailView.as_view(), name='order-detail'),




]