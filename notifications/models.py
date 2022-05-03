from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SendMail(models.Model):
    send_user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    send_users=models.ManyToManyField(User, related_name='send_emails_users', blank=True)
    content = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)

