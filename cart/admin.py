from .models import (
    Address,
    Product,
    Order, 
    OrderItem, 
    ColorVariation,
    SizeVariation,
)
from django.contrib import admin

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'address_type',
        'address_line_1',
        'address_line_2',
        'zip_code',
        'city',
    ]

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)
admin.site.register(Address, AddressAdmin)



