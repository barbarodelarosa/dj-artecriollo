from email.policy import default
from django.db import models
from django.urls import reverse
from shop.models import Product
from django.db.models.signals import pre_save
from django.utils.text import slugify

from django.contrib.auth import get_user_model

User = get_user_model()


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_finish = models.DateTimeField()
    price_init = models.FloatField(default=0.00)
    related_auction = models.ManyToManyField('self', blank=True)
    note = models.TextField(blank=True, null=True)
    aprobated = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    purchused = models.BooleanField(default=False)
    purchused_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="purchused_by")
    

    

    def __str__(self):
        return self.product.title

    def get_absolute_url(self):
        return reverse("auction:auction-detail", kwargs={'pk':self.pk})


class UserBid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    bid_amount = models.FloatField(default=0.00)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    winner = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'




def pre_safe_auction_receiver(sender, instance, *args, **kwargs):
    product = instance.product.id
    product = Product.objects.get(id = instance.product.id)
    product.for_auction = True
    product.save()
pre_save.connect(pre_safe_auction_receiver, sender=Auction)