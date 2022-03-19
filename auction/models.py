from email.policy import default
from django.db import models
from django.urls import reverse
from shop.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Auction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField()
    price_init = models.FloatField(default=0.00)
    related_auction = models.ManyToManyField('self', blank=True)
    

    def __str__(self):
        return self.product.title

    def get_absolute_url(self):
        return reverse("auction:auction-detail", kwargs={'pk':self.pk})


class UserBid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    bid_amount = models.FloatField(default=0.00)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'