# from authy.models import PeopleList
from django.urls import path, re_path
from profile.views import(EditProfile, UpdateProfileView, addOrRemoveToWhishList, OrderDetailView,
 addToList, PeopleListView, ListPeopleDelete, affiliateApplication, product_file_view, referedCode)
# ShowList, 

from django.contrib.auth import views as authViews 
app_name='profile'


urlpatterns = [
   	
    # path('profile/edit', EditProfile, name='edit-profile'),
    path('profile/<pk>/edit', UpdateProfileView.as_view(), name='edit-profile'),
    path('solicitar-afiliado/', affiliateApplication, name='solicitar-afiliado'),
    path('profile/addtolist', addToList, name='add-to-list'),
    path('ref-code/<str:ref_code>/', referedCode, name='ref-code'), #Enviar en la solicitud el codigo de usuario y la url a la que sera redirigido
    path('order/<pk>', OrderDetailView.as_view(), name='order-detail'),

   	path('mylists/<list_id>', PeopleListView, name='people-list'),
   	path('mylists/<list_id>/delete', ListPeopleDelete, name='list-people-delete'),
   	path('addorremovetowhishlist/<product>', addOrRemoveToWhishList, name='addorremovetowhishlist'),
	re_path(r"^download-file/(?P<pk>[a-zA-Z0-9_-]+)/$", product_file_view, name="product_file_view",),
	# re_path(r"^download-file-url/(?P<pk>[a-zA-Z0-9_-]+)/$", ProductDownloadURL.as_view(), name="product_download_url",),
	
   	
       
       # path('signup/', Signup, name='signup'),
   	# path('login/', authViews.LoginView.as_view(template_name='registration/login.html'), name='login'),
   	# path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
   	# path('changepassword/', PasswordChange, name='change_password'),
   	# path('changepassword/done', PasswordChangeDone, name='change_password_done'),
   	# path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
   	# path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
   	# path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   	# path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

   	# path('mylists', ShowList, name='show-my-lists'),
	
	
	


]