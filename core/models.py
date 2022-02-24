from django.db import models

# Create your models here.
class SiteInfo(models.Model):
    name = models.CharField(max_length=25, default='ArteCriollo')
    logo = models.ImageField(upload_to='image/logo')
    icon = models.ImageField(upload_to='image/icon')
    email = models.EmailField(max_length=30, default='artecriollocuba@gmail.com')
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, default='+5351183924')
    mobile = models.CharField(max_length=11, default='+5351183924')
    description = models.TextField(max_length=250, blank=True, null=True)
    