from dataclasses import field
from django import forms
from requests import models
from .models import NewsletterUser, Newsletter


class NewsletterUserSigUpForm(forms.ModelForm):
    class Meta:
        model = NewsletterUser
        fields = ['email']

class NewsletterCreationForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields=['name','subject','body','email']