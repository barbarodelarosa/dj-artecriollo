from django import template

register = template.Library()

@register.filter
def price_format_cup(price):
    new_format_price = price / 100
    print(new_format_price)
    return "${0:.2f} CUP".format(price / 100)