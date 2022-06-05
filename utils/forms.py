from django import forms 
from .models import SomeLocationModel  

class LocationForm(forms.ModelForm):  
    class Meta:  
        model = SomeLocationModel 
        fields = "__all__" 
