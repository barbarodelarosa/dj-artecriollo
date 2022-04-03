from django import template
# from cart.utils import get_or_set_order_session
from profile.models import Profile
from shop.models import WhishList
register = template.Library()

@register.filter
def whishlist_count(request):
    # order = get_or_set_order_session(request)
    if request.user.is_authenticated:
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)
        if created:
            whishlist = WhishList(user=user)
            whishlist.save()
        count = profile.whishlist.count()
        
        
        # try:
        #    whishlist = Profile.objects.get(user=user)
        # except Profile.DoesNotExist:
        #     whishlist = WhishList(user=user)
        #     whishlist.save()
        # count = whishlist.products.count()
        # return count

        # print(whishlist)
        # if not whishlist:
        #     whish = WhishList.objects.create(user=user)
        #     print(whish)
        #     whishlist = WhishList.objects.get(user=user)
        #     count = whishlist.products.count()
    count = 0
    return count