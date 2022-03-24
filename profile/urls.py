# from authy.models import PeopleList
from django.urls import path, re_path
from profile.views import EditProfile, addOrRemoveToWhishList, addToList, PeopleListView, ListPeopleDelete, product_file_view, ProductDownloadURL
# ShowList, 

from django.contrib.auth import views as authViews 
app_name='profile'


urlpatterns = [
   	
    path('profile/edit', EditProfile, name='edit-profile'),
    path('profile/addtolist', addToList, name='add-to-list'),

   	path('mylists/<list_id>', PeopleListView, name='people-list'),
   	path('mylists/<list_id>/delete', ListPeopleDelete, name='list-people-delete'),
   	path('addorremovetowhishlist/<product>', addOrRemoveToWhishList, name='addorremovetowhishlist'),
	re_path(r"^download-file/(?P<pk>[a-zA-Z0-9_-]+)/$", product_file_view, name="product_file_view",),
	re_path(r"^download-file-url/(?P<pk>[a-zA-Z0-9_-]+)/$", ProductDownloadURL.as_view(), name="product_download_url",),
	
   	
       
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