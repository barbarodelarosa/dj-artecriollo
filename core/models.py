from email.policy import default
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.shortcuts import reverse
from django.db.models.signals import pre_save




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
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, null=True)
    content = RichTextField()

    def __str__(self):
        return self.name


def pre_safe_page_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
pre_save.connect(pre_safe_page_receiver, sender=Page)
