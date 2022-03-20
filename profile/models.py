from dbm.ndbm import library
from itertools import product
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product, PurchasedProduct

from django.db.models.signals import post_save

from PIL import Image
from django.conf import settings
import os

def user_directory_path_profile(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

    return profile_pic_name

def user_directory_path_banner(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    banner_pic_name = 'user_{0}/banner.jpg'.format(instance.user.id)
    full_path = os.path.join(settings.MEDIA_ROOT, banner_pic_name)

    if os.path.exists(full_path):
    	os.remove(full_path)

#Posiblemente a cambiar por  profile_pic_name
    return banner_pic_name 

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	url = models.CharField(max_length=80, null=True, blank=True)
	profile_info = models.TextField(max_length=150, null=True, blank=True)
	created = models.DateField(auto_now_add=True)
	whishlist = models.ManyToManyField(Product, related_name="whishlist_user", blank=True)
	phone = models.CharField(max_length=11, blank=True, null=True)
	# favorites = models.ManyToManyField(Post)

	# picture = models.ImageField(upload_to=user_directory_path_profile, blank=True, null=True, verbose_name='Picture')
	# banner = models.ImageField(upload_to=user_directory_path_banner, blank=True, null=True, verbose_name='Banner')

	# def save(self, *args, **kwargs):
	# 	super().save(*args, **kwargs)
	# 	SIZE = 250, 250

	# 	if self.picture:
	# 		pic = Image.open(self.picture.path)
	# 		pic.thumbnail(SIZE, Image.LANCZOS)
	# 		pic.save(self.picture.path)

	def __str__(self):
		return self.user.username
		

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


class PeopleList(models.Model):
	title = models.CharField(max_length=150)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='list_user')
	people = models.ManyToManyField(User, related_name='people_user')	

	def __str__(self):
		return self.title



class UserLibrary(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='library')
	products = models.ManyToManyField(Product, blank=True)

	class Meta:
		verbose_name_plural = 'User Libraries'

		
	def __str__(self):
		return self.user.email
		

def post_save_user_riceiver(sender, instance, created, **kwargs):
	if created:
		library = UserLibrary.objects.create(user=instance)
	
	purchased_products = PurchasedProduct.objects.filter(email=instance.email)

	for purchased_product in purchased_products:
		library.products.add(purchased_product.product)

	
post_save.connect(post_save_user_riceiver, sender=User)
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)