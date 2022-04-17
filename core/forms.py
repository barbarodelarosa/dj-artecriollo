from core.models import Contact
from django import forms


class ContactForm(forms.Form):
    
    name = forms.CharField(max_length=100, label='Nombre', widget=forms.TextInput(attrs={
        'placeholder': "Tu Nombre",
    }))
    email = forms.EmailField(label='Correo', widget=forms.TextInput(attrs={
        'placeholder': "Tu Correo Electronico"
    }))
    message = forms.CharField(max_length=100, label='Mensaje', widget=forms.TextInput(attrs={
        'placeholder': "Tu Mensaje"
    }))
