from django import template

register = template.Library()

@register.simple_tag
def discount(total, part):
    part = part / 100
    total = total / 100
    porcent = part * 100 / total
    return "-{0:.0f}%".format(porcent)