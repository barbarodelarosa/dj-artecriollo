from unicodedata import category
from django import template
from shop.models import Category

register = template.Library()

@register.simple_tag()
def categories_list_tag():
    categories = Category.objects.all()
    print("categories")
    print(categories)
    return categories