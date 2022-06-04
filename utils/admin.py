from django.contrib import admin
from .models import Userip, VisitNumber, DayNumber
from .models import SomeLocationModel
from mapbox_location_field.admin import MapAdmin   
  
admin.site.register(SomeLocationModel, MapAdmin)  

admin.site.register(Userip)
admin.site.register(VisitNumber)
admin.site.register(DayNumber)
# Register your models here.
