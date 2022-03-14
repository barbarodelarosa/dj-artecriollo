from distutils.command.upload import upload
from tokenize import blank_re
from django.db import models
from ckeditor.fields import RichTextField

from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.auth.models import User
import datetime
User = get_user_model()


import base64


def image_directory_path(instance, filename):  
    return 'blog/{0}'.format(instance.name, filename)


class Category(models.Model):
    name=models.CharField(max_length=25)
    slug=models.SlugField(max_length=50, unique=True, blank=True, null=True)
    image=models.ImageField(upload_to=image_directory_path, blank=True, null=True)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("blog:category", kwargs={'slug': self.slug})



class Tag(models.Model):
    name=models.CharField(max_length=25)
    slug=models.SlugField(max_length=50, unique=True, blank=True, null=True)
    image=models.ImageField(upload_to=image_directory_path, blank=True, null=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:tag-detail", kwargs={'slug': self.slug})


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name="category_post")
    tag = models.ManyToManyField(Tag, related_name="tag_post")
    name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50, unique=True, blank=True, null=True)
    image=models.ImageField(upload_to=image_directory_path)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like=models.IntegerField(default=0)
    related_post = models.ManyToManyField('self', blank=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={'category': self.category.first().slug, 'slug': self.slug})



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
        slug_exists = Post.objects.filter(slug=instance.slug).exists()
        if  slug_exists:
             instance.slug = instance.slug+'-'+str(datetime.datetime.now())
pre_save.connect(pre_save_post_receiver, sender=Post)



def pre_safe_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
        slug_exists = Category.objects.filter(slug=instance.slug).exists()
        if  slug_exists:
             instance.slug = instance.slug+'-'+str(datetime.datetime.now())
pre_save.connect(pre_safe_category_receiver, sender=Category)


def pre_safe_tag_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
        slug_exists = Tag.objects.filter(slug=instance.slug).exists()
        if  slug_exists:
             instance.slug = instance.slug+'-'+str(datetime.datetime.now())
pre_save.connect(pre_safe_tag_receiver, sender=Tag)
