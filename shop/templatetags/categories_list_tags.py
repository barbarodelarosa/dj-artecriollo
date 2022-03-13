from unicodedata import category
from django import template
from shop.models import Category

register = template.Library()

@register.simple_tag()
def categories_list_tag():
    categories = Category.objects.all()
    return categories



@register.simple_tag()
def categories_list_for_footer():
    categories = Category.objects.all()[:6]
    return categories