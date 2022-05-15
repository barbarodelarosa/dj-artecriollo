from django.contrib import admin

from .models import UserBid, Auction

class AuctionAdmin(admin.ModelAdmin):
    list_display = ('product', 'aprobated', 'active','purchused','purchused_by')

admin.site.register(UserBid)
admin.site.register(Auction, AuctionAdmin)
