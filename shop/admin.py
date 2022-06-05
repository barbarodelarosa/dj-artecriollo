from affiliate.models import Shortener
from .models import *
from django.contrib import admin

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        
        'address_type',
        'address_line_1',
        'address_line_2',
        # 'zip_code',
        'city',
    ]
class CategoryAdmin(admin.ModelAdmin):
    search_fields=['name']

class MerchantAdmin(admin.ModelAdmin):
    search_fields=['name']

    



class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields=['category','related_products']

    # def save_model(self, request, obj, form, change):
    #     if obj.url_short:
    #         exist_url_short = Shortener.objects.filter(long_url=obj.get_absolute_url()).exists()
      
    #     else:
    #     # if exist_url_short:
    #         print("ABSOLUTE",obj.get_absolute_url())
    #         shortener = Shortener.objects.create(long_url=obj.get_absolute_url())
    #         url_short = request.build_absolute_uri('/') + 'u/' + shortener.short_url
    #         obj.url_short = url_short
    #         shortener.save()
    #         print("url_short", url_short)
    #         print("shortener", shortener)
    #     print("OBJ", obj)
    #     super(ProductAdmin, self).save_model(request, obj, form, change)
    


# Register your models here.
admin.site.register(Brand)
admin.site.register(Pais)
admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Provincia)
admin.site.register(Municipio)
admin.site.register(Localidad)
admin.site.register(ProductImagesContent)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Cupon)
admin.site.register(Product, ProductAdmin)
admin.site.register(WhishList)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)
admin.site.register(Address, AddressAdmin)
admin.site.register(Payment)
admin.site.register(PurchasedProduct)



