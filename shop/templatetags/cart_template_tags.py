from django import template
from shop.utils import get_or_set_order_session

register = template.Library()

@register.filter
def cart_item_count(request):
    order = get_or_set_order_session(request)
    count = order.items.count()
    return count


@register.filter
def cart_item_order(request):
    order = get_or_set_order_session(request)
    items = order.items.all()
    return items

@register.filter
def cart_item_order_subtotal_price(request):
    order = get_or_set_order_session(request)
    total = order.get_subtotal()
    return total

