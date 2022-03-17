from django.contrib import admin

from .models import UserBid, Auction

admin.site.register(UserBid)
admin.site.register(Auction)
