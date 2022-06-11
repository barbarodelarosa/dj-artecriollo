from email.policy import default
from statistics import mode
from django.db import models
from ckeditor.fields import RichTextField
from django.forms import DateTimeField
from django.utils.text import slugify
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.contrib.auth.models import User




# Create your models here.
class SiteInfo(models.Model):
    name = models.CharField(max_length=25, default='ArteCriollo')
    logo = models.ImageField(upload_to='image/logo', default='/static/images/logo.png')
    icon = models.ImageField(upload_to='image/icon', default='/static/images/logo.png')
    email = models.EmailField(max_length=30, default='artecriollocuba@gmail.com')
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, default='+5351183924')
    mobile = models.CharField(max_length=11, default='+5351183924')
    description = models.TextField(max_length=250, blank=True, null=True)


class SocialRed(models.Model):
    icon = models.ImageField(upload_to='image/socialred/icon', blank=True, null=True)
    logo = models.ImageField(upload_to='image/socialred/logo',blank=True, null=True)
    name = models.CharField(max_length=25)
    name_user = models.CharField(max_length=25)
    url = models.URLField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Page(models.Model):
    image=models.ImageField(upload_to="pages", blank=True, null=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, null=True, unique=True)
    content = RichTextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Page, self).save(*args, **kwargs)

    def get_absolute_url(self):       
        return reverse("page-detail", kwargs={'slug': self.slug})


class Contact(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField(max_length=25)
    message = models.TextField()

    def __str__(self):
        return f'{self.name} - {self.email}'

def pre_safe_page_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
pre_save.connect(pre_safe_page_receiver, sender=Page)




class NotificationUser(models.Model):
    TYPE_NOTIFICATION_CHOICE={
        ('ONE_USER','ONE_USER'),
        ('GROUP_USER','GROUP_USER'),
        ('ALL_USER','ALL_USER'),
        ('ALL_USER_AUTHENTICATED','ALL_USER_AUTHENTICATED'),
    }
    type=models.CharField(max_length=22, choices=TYPE_NOTIFICATION_CHOICE)
    message = models.CharField(max_length=160)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    readed_at=models.DateTimeField(blank=True, null=True)
    readed_for=models.ManyToManyField(User, blank=True)
    readed=models.BooleanField(default=False)
    active=models.BooleanField(default=False)
    def __st__(self):
        return self.message