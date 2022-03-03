from shop.models import WhishList
from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import NewListForm, SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from authy.models import PeopleList, Profile
# , PeopleList
# from authy.forms import NewListForm
# from post.models import Post, Follow, Stream
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.core.paginator import Paginator

from django.urls import resolve

# from tier.models import Subscription, Tier

def SideNavInfo(request):
	user = request.user
	nav_profile = None
	fans = None
	follows = None

	if user.is_authenticated:
		nav_profile = Profile.objects.get(user=user)
		fans = Subscription.objects.filter(subscribed=user).count()
		follows = Subscription.objects.filter(subscriber=user).count()

		print(nav_profile.user)

		return{"nav_profile": nav_profile, "fans":fans, "follows":follows}

# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	tiers = Tier.objects.filter(user=user)

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


def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('user:edit-profile')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'registration/signup.html', context)


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form':form,
	}

	return render(request, 'registration/change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	user_basic_info = User.objects.get(id=user)
	# BASE_WIDTH = 400

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.banner = form.cleaned_data.get('banner')
			user_basic_info.first_name = form.cleaned_data.get('first_name')
			user_basic_info.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			user_basic_info.save()
			return redirect('edit-profile')
	else:
		form = EditProfileForm(instance=profile)

	context = {
		'form':form,
	}

	return render(request, 'registration/edit_profile.html', context)


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


def RemoveFromList(request, username):
	person = get_object_or_404(User, username=username)
	list_id = PeopleList.objects.get(user=request.user, people=person)
	try:
		PeopleList.people.through.objects.filter(user_id=person.id, peoplelist_id=list_id).delete()
		return HttpResponseRedirect(reverse('user:profile', args=[person]))
	except Exception as e:
		raise e

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



def PeopleListView(request, list_id):		
	user_list = get_object_or_404(PeopleList, id=list_id)

	context = {
		'user_list': user_list,
	}

	return render(request, 'people_list.html', context)

def ListPeopleDelete(request, list_id):
	PeopleList.objects.filter(id=list_id).delete()
	return HttpResponseRedirect(reverse('profile', args=[request.user.username]))




@login_required
def addOrRemoveToWhishList(request, product):
	user = request.user
	profile = get_object_or_404(Profile, user=user)
	next = request.META.get('HTTP_REFERER', None) or '/'
	print("profile")
	print(profile)
	print(product)
	print("profile.whishlist")
	print(profile.whishlist.filter(id=product).exists())
	print("profile.whishlist")
	if profile.whishlist.filter(id=product).exists():
		profile.whishlist.remove(product)
	else:
		profile.whishlist.add(product)

	return HttpResponseRedirect(next)
