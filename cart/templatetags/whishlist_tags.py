from django import template
# from cart.utils import get_or_set_order_session
from cart.models import WhishList
register = template.Library()

@register.filter
def whishlist_count(request):
    # order = get_or_set_order_session(request)
    user = request.user
    whishlist = WhishList.objects.get(user=user)
    count = whishlist.products.count()
    return count