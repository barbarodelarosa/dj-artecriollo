from django import template
from core.models import Page, SiteInfo
from auction.models import Auction
from lottery.models import Lottery

register = template.Library()

@register.simple_tag()
def site_info():
    info        = SiteInfo.objects.get(id=1)
    phone       = info.phone
    email       = info.email
    address     = info.address
    description = info.description
    data = {
        'phone'      :phone,
        'email'      :email,
        'address'    :address,
        'description':description
    }
    return data

@register.simple_tag()
def auction():
    auction = Auction.objects.all()
    return auction


@register.simple_tag()
def lottery():
    lottery = Lottery.objects.all()
    return lottery


@register.simple_tag()
def pages():
    pages = Page.objects.filter(active=True)
    return pages