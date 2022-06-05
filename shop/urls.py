from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name='shop'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='home', permanent=False)),
    path('create-product/', views.CreateProductView.as_view(), name='create-product'),
    path('create-digital-product/', views.CreateDigitalProductView.as_view(), name='create-digital-product'),
    path('create-merchant/', views.CreateMerchantView.as_view(), name='create-merchant'),
    path('cart/', views.CartView.as_view(), name='summary'),
    path('cart/<product_id>/add/', views.addToCart, name='add-to-cart'), #No funciona todavia
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    # path('category/<category>/', views.CategoryDeatilView.as_view(), name='category-detatil'),
    
    path('whishlist/', views.WhishlistView.as_view(), name='whishlist'),
    # path('whishlist/<product_id>', views.AddOrRemoveToWhishlist.as_view(), name='add-remove-whishlist'),
    
    # path('<slug>', views.CategoryDeatilView.as_view(), name='category-detail'),
    path('increase-quantity/<pk>/', views.IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<pk>/', views.DecreaseQuantityView.as_view(), name='decrease-quantity'),
    path('remove-from-cart/<pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('payment-enzona/', views.ConfirmEnzonaPaymentView.as_view(), name='payment-enzona'),
    path('payment-enzona-digital-product/<pk>', views.EnzonaPaymentDigitalProductView.as_view(), name='payment-enzona-digital-product'),
    # path('payment-cash/', views.ConfirmCashPaymentView.as_view(), name='payment-cash'),
    path('confirm-order/', views.ConfirmOrderView.as_view(), name='confirm-order'),
    path('thankyou/', views.ThankYouView.as_view(), name='thankyou'),
    # path('orders/<pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('<slug>/', views.ProductListView.as_view(), name='product-list'),
    path('<category>/<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('actualizar_costo_mensajeria', views.actualizar_costo_mensajeria, name='actualizar_costo_mensajeria'), #CAMBIAR URL EN CHECKOUT (PETICION AJAX)





]