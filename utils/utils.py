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