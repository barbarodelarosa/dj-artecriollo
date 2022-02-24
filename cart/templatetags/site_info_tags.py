from django import template
from core.models import SiteInfo

register = template.Library()

@register.simple_tag()
def site_info():
    info    = SiteInfo.objects.get(id=1)
    phone   = info.phone
    email   = info.email
    address = info.address
    data = {
        'phone'  :phone,
        'email'  :email,
        'address':address
    }
    return data