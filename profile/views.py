from profile.forms import AffiliateApplicationForm
from shop.models import Order, WhishList, Product
from django.shortcuts import render, redirect, get_object_or_404
# from profile.forms import NewListForm, EditProfileForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, View



from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from profile.models import AffiliateApplication, PeopleList, Profile
# , PeopleList
# from profile.forms import NewListForm
# from post.models import Post, Follow, Stream
from django.db import transaction
from django.template import loader
from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator

from django.urls import resolve, reverse

from django_downloadview import ObjectDownloadView
from django_downloadview import HTTPDownloadView

# ******************

# import functools

# from django.conf import settings
# from django.views.generic import DetailView

# from django_weasyprint import WeasyTemplateResponseMixin
# from django_weasyprint.views import WeasyTemplateResponse
# ********************


# from tier.models import Subscription, Tier

# def SideNavInfo(request):
# 	user = request.user
# 	nav_profile = None
# 	fans = None
# 	follows = None

# 	if user.is_authenticated:
# 		nav_profile = Profile.objects.get(user=user)
# 		fans = Subscription.objects.filter(subscribed=user).count()
# 		follows = Subscription.objects.filter(subscriber=user).count()

# 		print(nav_profile.user)

# 		return{"nav_profile": nav_profile, "fans":fans, "follows":follows}

# Create your views here.
@login_required()
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	# tiers = Tier.objects.filter(user=user)

	#Favorite people lists select
	favorite_list = PeopleList.objects.filter(user=request.user)

	#Check is the profile is in any people list
	person_in_list = PeopleList.objects.filter(user=request.user, people=user).exists()


	#New favorite List form
	#form_class = NewListForm
	 # if request is not post, initialize an empty form
	form = NewListForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		#form = NewListForm(request.POST)
		#if form.is_valid:
		title = form.cleaned_data['title']
		PeopleList.objects.create(title=title, user=request.user)
		return HttpResponseRedirect(reverse('profile', args=[username]))
	else:
		form = NewListForm()
	# url_name = resolve(request.path).url_name
	
	# if url_name == 'profile':
	# 	posts = Post.objects.filter(user=user).order_by('-posted')

	# else:
	# 	posts = profile.favorites.all()

	# #Profile info box
	# posts_count = Post.objects.filter(user=user).count()
	# following_count = Follow.objects.filter(follower=user).count()
	# followers_count = Follow.objects.filter(following=user).count()

	# #follow status
	# follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	# #Pagination
	# paginator = Paginator(posts, 8)
	# page_number = request.GET.get('page')
	# posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		# 'posts': posts_paginator,
		'profile':profile,
		# 'following_count':following_count,
		# 'followers_count':followers_count,
		# 'posts_count':posts_count,
		# 'follow_status':follow_status,
		# 'url_name':url_name,
		'tiers': tiers,
		'form': form,
		'favorite_list': favorite_list,
		'person_in_list': person_in_list,
	}

	return HttpResponse(template.render(context, request))

# def UserProfileFavorites(request, username):
# 	user = get_object_or_404(User, username=username)
# 	profile = Profile.objects.get(user=user)
	
# 	posts = profile.favorites.all()

# 	#Profile info box
# 	posts_count = Post.objects.filter(user=user).count()
# 	following_count = Follow.objects.filter(follower=user).count()
# 	followers_count = Follow.objects.filter(following=user).count()

# 	#Pagination
# 	paginator = Paginator(posts, 8)
# 	page_number = request.GET.get('page')
# 	posts_paginator = paginator.get_page(page_number)

# 	template = loader.get_template('profile_favorite.html')

# 	context = {
# 		'posts': posts_paginator,
# 		'profile':profile,
# 		'following_count':following_count,
# 		'followers_count':followers_count,
# 		'posts_count':posts_count,
# 	}

# 	return HttpResponse(template.render(context, request))




from django.contrib import messages

@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	user_basic_info = User.objects.get(id=user)

	# BASE_WIDTH = 400

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			print("HASTA AQUI OK")
			# profile.picture = form.cleaned_data.get('picture')
			# profile.banner = form.cleaned_data.get('banner')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.phone = form.cleaned_data.get('phone')
			profile.save()
			# user_basic_info.save()
			
			messages.success(
				request, "Se ha actualizado correctamente su perfil"
			)
			return redirect('user:edit-profile')
	else:
		form = EditProfileForm(instance=profile)

	context = {
		'form':form,
	}

	return render(request, 'account/edit_profile.html', context)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
	model = Profile
	fields=['first_name','last_name','profile_info','phone','ci','gender']
	success_url='/profile/'
	template_name='account/edit_profile.html'




# @login_required
# def follow(request, username, option):
# 	following = get_object_or_404(User, username=username)

# 	try:
# 		f, created = Follow.objects.get_or_create(follower=request.user, following=following)

# 		if int(option) == 0:
# 			f.delete()
# 			Stream.objects.filter(following=following, user=request.user).all().delete()
# 		else:
# 			 posts = Post.objects.all().filter(user=following)[:25]

# 			 with transaction.atomic():
# 			 	for post in posts:
# 			 		stream = Stream(post=post, user=request.user, date=post.posted, following=following)
# 			 		stream.save()

# 		return HttpResponseRedirect(reverse('profile', args=[username]))
# 	except User.DoesNotExist:
# 		return HttpResponseRedirect(reverse('profile', args=[username]))


@login_required()
def addToList(request):
	user = request.user

	if request.method == 'POST':
		to_list = request.POST.get('list_item')
		to_person = request.POST.get('to')
		print(str(to_person))
		person = get_object_or_404(User, username=to_person)

		try:
			people_list = get_object_or_404(PeopleList, user=user, id=to_list)
			people_list.people.add(person)
			print('Hasta aqui todo OK')
			return HttpResponseRedirect(reverse('user:profile', args=[to_person]))
		except Exception as e:
			raise e



@login_required()
def RemoveFromList(request, username):
	person = get_object_or_404(User, username=username)
	list_id = PeopleList.objects.get(user=request.user, people=person)
	try:
		PeopleList.people.through.objects.filter(user_id=person.id, peoplelist_id=list_id).delete()
		return HttpResponseRedirect(reverse('user:profile', args=[person]))
	except Exception as e:
		raise e

@login_required()
def ShowList(request):
	user_lists = PeopleList.objects.filter(user=request.user)


	form = NewListForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		#form = NewListForm(request.POST)
		#if form.is_valid:
		title = form.cleaned_data['title']
		PeopleList.objects.create(title=title, user=request.user)
		return HttpResponseRedirect(reverse('user:profile', args=[request.user.username]))
	else:
		form = NewListForm()

	context = {
		'user_lists':user_lists,
		'form': form
	}

# 	return render(request, 'user_lists.html', context)



@login_required()
def PeopleListView(request, list_id):		
	user_list = get_object_or_404(PeopleList, id=list_id)

	context = {
		'user_list': user_list,
	}

	return render(request, 'people_list.html', context)



@login_required()
def ListPeopleDelete(request, list_id):
	PeopleList.objects.filter(id=list_id).delete()
	return HttpResponseRedirect(reverse('profile', args=[request.user.username]))




@login_required()
def addOrRemoveToWhishList(request, product):
	user = request.user
	profile = get_object_or_404(Profile, user=user)
	next = request.META.get('HTTP_REFERER', None) or '/'

	if profile.whishlist.filter(id=product).exists():
		profile.whishlist.remove(product)
	else:
		profile.whishlist.add(product)

	return HttpResponseRedirect(next)




product_file_view = ObjectDownloadView.as_view(model=Product, file_field="content_file")

#SOLO FUNCIONA PARA DESCARGAR IMAGEN
# class ProductDownloadURL(LoginRequiredMixin, HTTPDownloadView):
#     #PENSE QUE NO RESOLVERIA ESTE PROBLEMA TAN SENCILLO
# 	def get_url(self):
	
# 		pk =self.kwargs.get('pk')
# 		product = Product.objects.get(pk=pk)
	
# 		self.url = product.content_url
# 		return self.url



def referedCode(request, *args, **kwargs):

	code = str(kwargs.get('ref_code'))
	next_url = str(request.GET.get('next_url'))

	try:
		profile = Profile.objects.get(code=code)
		
		request.session['ref_profile']=profile.id

	except:
		pass
	
	url = request.build_absolute_uri()
	# print("URL REFER")
	# print(next_url)
	return HttpResponseRedirect(next_url)



@login_required()
def affiliateApplication(request):
	profile = Profile.objects.get(user=request.user)
	if profile.phone and profile.ci:

		form = AffiliateApplicationForm(request.POST or None)
		if request.method == 'POST' and form.is_valid():
			
			# profile = form.cleaned_data['profile']
			
			AffiliateApplication.objects.create(profile=profile)

			messages.info(request, "Solicitud enviada")
			return HttpResponseRedirect(reverse('profile'))

		else:
			messages.info(request, "Error al enviar la solicitud, por favor revisar los requisitos")
			return HttpResponseRedirect(reverse('profile'))
	else:
		messages.error(request, "Antes de solicitar la cuenta de afilidado, debe editar su perfil y agregar su numero de telefono y CI")
		return HttpResponseRedirect(reverse('profile'))

class OrderDetailView(LoginRequiredMixin, generic.DetailView):
	template_name='order.html'
	queryset=Order.objects.all()
	#****************************************************************************************************
	# La funcion establece que si el usuario no es el propietario da error 404 (no encuentra la pagina) #
	#****************************************************************************************************

	def get_queryset(self):
         queryset = super(OrderDetailView, self).get_queryset()
         return queryset.filter(user=self.request.user)
		 

# class CustomWeasyTemplateResponse(WeasyTemplateResponse):
#     # customized response class to change the default URL fetcher
#     def get_url_fetcher(self):
#         # disable host and certificate check
#         context = ssl.create_default_context()
#         context.check_hostname = False
#         context.verify_mode = ssl.CERT_NONE
#         return functools.partial(django_url_fetcher, ssl_context=context)

# class PrintView(WeasyTemplateResponseMixin, OrderDetailView):
#     # output of MyDetailView rendered as PDF with hardcoded CSS
#     pdf_stylesheets = [
#         settings.STATIC_ROOT + 'new/css/bootstrap.css',
#     ]
#     # show pdf in-line (default: True, show download dialog)
#     pdf_attachment = False
#     # custom response class to configure url-fetcher
#     response_class = CustomWeasyTemplateResponse

# class DownloadView(WeasyTemplateResponseMixin, OrderDetailView):
#     # suggested filename (is required for attachment/download!)
#     pdf_filename = 'foo.pdf'

# class DynamicNameView(WeasyTemplateResponseMixin, MyDetailView):
#     # dynamically generate filename
#     def get_pdf_filename(self):
#         return 'foo-{at}.pdf'.format(
#             at=timezone.now().strftime('%Y%m%d-%H%M'),
#         )