from django.shortcuts import render
from django.views.generic import CreateView
from .forms import *

# Create your views here.

from .models import *
from django.utils import timezone

#Función personalizada, no vista
def change_info(request):       #Modificar información como visitas al sitio web y visitar ip
    # Por cada visita, agregue 1 al número total de visitas al sitio web
    count_nums = VisitNumber.objects.filter(id=1)   
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = VisitNumber()
        count_nums.count = 1
    count_nums.save()

    # Registre el número de visitas a ip y cada ip
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # Obtener ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # Así que aquí está la ip real
    else:
        client_ip = request.META['REMOTE_ADDR']  # Obtenga proxy ip aquí
    # print(client_ip)

    ip_exist = Userip.objects.filter(ip=str(client_ip))
    if ip_exist:  # Determinar si existe la ip
        uobj = ip_exist[0]
        uobj.count += 1
    else:
        uobj = Userip()
        uobj.ip = client_ip
        uobj.count = 1
    uobj.save()

    # Incrementar las visitas de hoy
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date)
    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.count = 1
    temp.save()


class SomeLocationModelView(CreateView):
    form_class = LocationForm
    template_name= "maps/index.html"
    success_url='/utils/maps'