from django import template
from core.models import SocialRed

register = template.Library()

@register.simple_tag()
def social_red():
    return SocialRed.objects.all()

