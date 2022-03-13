# from authy.models import PeopleList
from django.urls import path
from profile.views import EditProfile, addOrRemoveToWhishList, addToList, PeopleListView, ListPeopleDelete
# ShowList, 

from django.contrib.auth import views as authViews 
app_name='profile'


urlpatterns = [
   	
    path('profile/edit', EditProfile, name='edit-profile'),
    path('profile/addtolist', addToList, name='add-to-list'),

   	path('mylists/<list_id>', PeopleListView, name='people-list'),
   	path('mylists/<list_id>/delete', ListPeopleDelete, name='list-people-delete'),
   	path('addorremovetowhishlist/<product>', addOrRemoveToWhishList, name='addorremovetowhishlist'),
   	
       
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