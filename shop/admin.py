from unicodedata import category
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



class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields=['category','related_products']


# Register your models here.
admin.site.register(Brand)
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Municipio)
admin.site.register(ProductImagesContent)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Product, ProductAdmin)
admin.site.register(WhishList)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)
admin.site.register(Address, AddressAdmin)
admin.site.register(Payment)



