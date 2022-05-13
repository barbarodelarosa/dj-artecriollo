from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SendMail(models.Model):

    name = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    body = models.TextField(blank=True, null=True)
    email_admin=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    send_users=models.ManyToManyField(User, related_name='send_emails_users', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)
    subscribe = models.BooleanField(default=True, blank=True, null=True)
    

class EmailNotification(models.Model):
    transmitter=models.ForeignKey(User, on_delete=models.CASCADE)
    receivers=models.ManyToManyField(User, related_name='receivers')
    created=models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    body = models.TextField(blank=True, null=True)
    readed = models.BooleanField(default=False)
    