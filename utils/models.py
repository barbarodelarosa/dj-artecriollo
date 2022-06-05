from django.db import models
from django.utils import timezone
from mapbox_location_field.models import LocationField, AddressAutoHiddenField
# from mapbox_location_field.spatial.models import SpatialLocationField  

# Dirección IP y número de visitas al sitio web
class Userip(models.Model):
    ip=models.CharField(verbose_name='Dirección IP',max_length=30)    #ip address
    count=models.IntegerField(verbose_name='Visitas',default=0) # Las visitas ip
    class Meta:
        verbose_name = 'Acceder a la información del usuario'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.ip

#Total de visitas al sitio web
class VisitNumber(models.Model):
    count=models.IntegerField(verbose_name='Total de visitas al sitio web',default=0) #Total de visitas al sitio web
    class Meta:
        verbose_name = 'Total de visitas al sitio web'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.count)

# Estadísticas de visitas de un día
class DayNumber(models.Model):
    day=models.DateField(verbose_name='Fecha',default=timezone.now)
    count=models.IntegerField(verbose_name='Número de visitas al sitio web',default=0) #Total de visitas al sitio web
    class Meta:
        verbose_name = 'Estadísticas de visitas diarias al sitio web'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.day)



class SomeLocationModel(models.Model):  
    address = AddressAutoHiddenField()  
    location = LocationField(
        map_attrs = {  
        "style": "mapbox://styles/mapbox/outdoors-v11",
        "zoom": 10,
        "center": [-82.38304, 23.13302], #Aqui va al reves de lo que se muestra en la pantalla(Longitud y Latitud)
        # "center": [17.031645, 51.106715],
        "cursor_style": 'pointer',
        "marker_color": "blue",
        "rotate": False,
        "geocoder": True,
        "fullscreen_button": True,
        "navigation_buttons": True,
        "track_location_button": True, 
        "readonly": True,
        "placeholder": "Elija una ubicación en el mapa a continuación", 
        "language": "auto",
        "message_404": "Dirección no definida", }
        
    )
  
