from .models import NotificationUser, Page, SiteInfo, SocialRed
from django.contrib import admin

# Register your models here.
admin.site.register(SiteInfo)
admin.site.register(SocialRed)
admin.site.register(Page)
admin.site.register(NotificationUser)