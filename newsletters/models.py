from django.db import models

# Create your models here.

class NewsletterUser(models.Model):
    email = models.EmailField(null=False, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    subscribe = models.BooleanField(default=True, blank=True, null=True)
    unsubscribe_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"Subcribe: {self.subscribe} | Email: {self.email} | Subscribed: {self.date_added.strftime('%d,%m,%Y')} | Unsubscribed: {self.unsubscribe_date.strftime('%d,%m,%Y')}"

    class Meta:
        ordering = ['-subscribe', '-date_added']


class Newsletter(models.Model):
    name = models.CharField(max_length=250)
    subject = models.CharField(max_length=250)
    body = models.TextField(blank=True, null=True)
    email = models.ManyToManyField(NewsletterUser)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
