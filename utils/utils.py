import requests
from django.contrib import messages

def testConnect(request):
    try:
        connect = requests.get("www.google.com", timeout=5)
    except (requests.ConnectionError, requests.Timeout):
        print("Sin conexión a internet.")
        return messages.error(request, 'No tienes conexión a internet :(')
    else:
        print("Con conexión a internet.")


def costo_envio(municipio):

    if municipio == 'ARROYO_NARANJO':
        envio = 5000
        return envio
    elif municipio == '10_DE_OCTUBRE':
        envio = 7500
        return envio
    elif municipio == 'CERRO':
        envio = 10000
        return envio
    elif municipio == 'LISA':
        envio = 12500
        return envio
    else:
        envio = 2000
        return envio
