from .models import EmailNotification, SendMail
from django.contrib import admin

admin.site.register(SendMail)
admin.site.register(EmailNotification)

# Register your models here.
