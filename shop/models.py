
from email.policy import default
from itertools import product
import os
from utils.utils import costo_envio
from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField

from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.auth.models import User

from artecriollo.utils import ResizeImageMixin


import base64


def user_directory_path(instance, filename):
    # print(filename)
    # params = (
    #     ('key', 'f97180bb3340aac89d470b207127ac0a'),
    # )
    # path_img = 'user_{0}/product_{1}'.format(instance.user.username, filename)
    # with open(path_img, "rb") as img_file:
    #     my_string = base64.b64encode(img_file.read())
    
    # print(my_string)

    # files = { 
    #     'image': (None, filename),
    # }


    # response = requests.post('https://api.imgbb.com/1/upload', params=params, files=files)
    # print(response)
    # return response
    # This file will be uploaded to MEDIA_ROOT/the user{id}/thefile
    if not filename:
        return None
    img_path = 'images_products/product_{0}'.format(filename)
    full_path = os.path.join(settings.MEDIA_ROOT, img_path)
    if os.path.exists(full_path):
        os.remove(full_path)
    return img_path

class ProductImagesContent(models.Model, ResizeImageMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner', blank=True, null=True)
    file = models.FileField(upload_to= user_directory_path)
    posted = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=125, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.resize(self.file, (350, 350))

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id}-{self.user.username}-{self.title}"

User = get_user_model()



class Merchant(models.Model, ResizeImageMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=25, blank=True, null=True, unique=True)
    logo = models.ImageField(upload_to="image/merchant", blank=True, null=True)
    image = models.ImageField(upload_to="image/merchant", blank=True, null=True)
    banner = models.ImageField(upload_to="image/merchant", blank=True, null=True)
    description=RichTextField()
    phone = models.CharField(max_length=11, blank=True, null=True)
    address = models.ForeignKey("Address", on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    aprobated = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):        
        return reverse("shop:merchant", kwargs={'slug': self.slug})




class Category(models.Model, ResizeImageMixin):
    image = models.ImageField(upload_to="image/category", blank=True, null=True) 
    name  = models.CharField(max_length=100)
    slug  = models.SlugField(unique=True, blank=True, null=True)
    short_name = models.CharField(max_length=12, blank=True, null=True)
    active= models.BooleanField(default=True)


    class Meta:
        verbose_name_plural = "Categories"

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product-list", kwargs={'slug': self.slug})




class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Tags"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


    def __str__(self):
        return self.name




class Pais(models.Model):
    name=models.CharField(max_length=50, default="CUBA")
    
    def __str__(self):
        return f'{self.name}'

class Provincia(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.name}'

class Municipio(models.Model):
    # pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    shipping = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return f'{self.name}'


class Localidad(models.Model):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    name=models.CharField(max_length=80)
    shipping = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return f'{self.name}'

  
class Address(models.Model):
    # ADDRESS_CHOICES = (
    #     ('B', 'Billing'),
    #     ('S', 'Shipping'),
    # )
    ADDRESS_CHOICES = (
        ('P', 'PARTICULAR'),
        ('E', 'ENVIO'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, blank=True, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, blank=True, null=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, blank=True, null=True)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE, blank=True, null=True)
    address_line_1 = models.CharField(max_length=150, blank=True, null=True)
    address_line_2 = models.CharField(max_length=150, blank=True, null=True)
    numero = models.CharField(max_length=8, blank=True, null=True)
    apt = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    # zip_code = models.CharField(max_length=10, blank=True, null=True)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES, blank=True, null=True)
    default = models.BooleanField(default=False)
    map_id = models.CharField(max_length=6, blank=True, null=True)
    map_latitude = models.FloatField(blank=True, null=True)
    map_langitude = models.FloatField(blank=True, null=True)
    map_address = models.CharField(max_length=50, blank=True, null=True)
  

    def __str__(self):
        return f"{self.user} | {self.provincia} | {self.municipio} | {self.address_line_1} | {self.address_line_2}"

    class Meta:
        verbose_name_plural = 'Addresses'
        ordering = ['provincia', 'municipio']


class ColorVariation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SizeVariation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Shop(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class MaterialVariation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name


class Product(models.Model, ResizeImageMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    merchant=models.ForeignKey(Merchant, on_delete=models.CASCADE, blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=150)
    product_images = models.ManyToManyField(ProductImagesContent, blank=True, related_name='images_product')
    slug = models.SlugField(unique=True, blank=True, max_length=150)
    url_short = models.URLField(blank=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    price = models.IntegerField(default=0)
    old_price = models.IntegerField(default=0, blank=True, null=True)
    description = models.TextField()
    details = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    aprobated = models.BooleanField(default=False)
    avialable_colours = models.ManyToManyField(ColorVariation, blank=True)
    avialable_sizes = models.ManyToManyField(SizeVariation,blank=True)
    stock = models.PositiveIntegerField(default=0)
    new = models.BooleanField(default=True)
    selling = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    content_url = models.URLField(blank=True, null=True)
    content_file = models.FileField(upload_to='products/content-files/', blank=True, null=True)
    for_auction = models.BooleanField(default=False)
    for_lottery = models.BooleanField(default=False)
    close_auction = models.DateTimeField(auto_now=True)
    selling_date = models.DateTimeField(auto_now=True)
    related_products = models.ManyToManyField('self', blank=True)

    
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title

    
    
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Product, self).save(*args, **kwargs)


    def get_price(self):
        price = self.price
        return "{:.2f}".format(price / 100)


    def get_absolute_url(self):
        category = self.category.first()
        
        return reverse("shop:product-detail", kwargs={'category': category.slug,'slug': self.slug})

class PurchasedProduct(models.Model):
    email = models.EmailField()
    product = models.ForeignKey(Product, models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email

class WhishList(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='whishlist_user')
    products = models.ManyToManyField(Product, blank=True, related_name='products_whishlist')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        category = self.category.first()
        
        return reverse("shop:whishlist", kwargs={'user': self.user})

class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    colour = models.ForeignKey(ColorVariation, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(SizeVariation, on_delete=models.CASCADE, blank=True, null=True)
    material = models.ForeignKey(MaterialVariation, on_delete=models.CASCADE, blank=True, null=True)
    tax = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)



             

    def __str__(self):
        return f"{self.quantity} % {self.product.title}"

    def get_tax(self):
        tax = self.tax
        return "{:.2f}".format(tax / 100)
    
    def get_raw_total_item_price(self):
        
        return self.quantity *  self.product.price

    """  def get_item_discount_price(self):
        price = self.get_raw_total_item_price()
        # price = price + self.discount
        return "{:.2f}".format(price / 100) """


    def get_total_item_price(self):
        price = self.get_raw_total_item_price()
        return "{:.2f}".format(price / 100)


class Order(models.Model):
    EFECTIVO='EFECTIVO'
    ENZONA='ENZONA'
    TRANSFERMOVIL='TRANSFERMOVIL'
    STATUS_CHOICES = (
        ('CONFIRMADO','CONFIRMADO'),
        ('EN PREPARACIÓN','EN PREPARACIÓN'),
        ('PREPARADO','PREPARADO'),
        ('ENTREGADO','ENTREGADO'),
        ('ANULADO','ANULADO'),
    )
    PAY_STATUS_CHOICES = (
        ('NO PAGADO','NO PAGADO'),
        ('AUTORIZADO','AUTORIZADO'),
        ('PAGADO','PAGADO'),
        ('ANULADO','ANULADO'),
    )
    PAYMENT_METHOD_CHOICES = (
        (EFECTIVO, 'EFECTIVO'),
        (ENZONA, 'ENZONA'),
        (TRANSFERMOVIL, 'TRANSFERMOVIL'),
    )
    DELIVERY_METHOD_CHOICES = (
        (1, 'DOMICILIO'),
        (2, 'RECOGIDA_LOCAL'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    shipping = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True, null=True)
    pay_status = models.CharField(max_length=15, choices=PAY_STATUS_CHOICES, blank=True, null=True)
    note=models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(max_length=25, blank=True, null=True)
    payment_method = models.CharField(max_length=13, choices=PAYMENT_METHOD_CHOICES, default=EFECTIVO)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHOD_CHOICES, default=1)
    user_recommended=models.ForeignKey(User, blank=True, null=True, related_name='user_recommended', on_delete=models.CASCADE)

    

    # billing_address = models.ForeignKey(
    #     Address, related_name='billing_address', blank=True, null=True, on_delete=models.SET_NULL
    # )
    shipping_address = models.ForeignKey(
        Address, related_name='shipping_address', blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.reference_number

    @property
    def reference_number(self):
        return f"ORDER-{self.pk}"

    def get_raw_subtotal(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_raw_total_item_price()
        return total

    def get_subtotal(self):
        subtotal = self.get_raw_subtotal()
        return "{:.2f}".format(subtotal / 100)

 

    def get_raw_total_tax(self):
        total_tax = 0
        for order_item in self.items.all():
            total_tax += order_item.tax
        return total_tax

    def get_total_tax(self):
        total_tax = self.get_raw_total_tax()
        return "{0:.2f}".format(total_tax / 100)

    def get_raw_total_shipping(self):
        if self.delivery_method == "1":
            return self.shipping
        else:
            return 0

    def get_total_shipping(self):
        shipping = self.get_raw_total_shipping()
        return "{0:.2f}".format(shipping / 100)



    def get_raw_total_discount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.discount
   
        total + self.discount
      
        return total

    def get_total_discount(self):
        total_discount = self.get_raw_total_discount() + self.discount
        return "{0:.2f}".format(total_discount / 100)


    def get_raw_total(self):
        subtotal = self.get_raw_subtotal()

        #Agregar suma de IVA, Delivery, Restar descuentos
        #total = subtotal - discount + tax + delivery
        #total = subtotal - discount + tax + delivery
        tax = self.get_raw_total_tax()
        discount = self.get_raw_total_discount()
        shipping = self.get_raw_total_shipping()
        discount = discount + self.discount
        print('discount')
        print(discount)
        subtotal = subtotal + tax + shipping - discount
        return subtotal

    def get_total(self):
        total = self.get_raw_total()
  
        return "{0:.2f}".format(total / 100)


class Payment(models.Model):
     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
     payment_method = models.CharField(max_length=20, choices=(
         ('EFECTIVO', 'EFECTIVO'),
         ('ENZONA', 'ENZONA'),
         ('TRANSFERMOVIL', 'TRANSFERMOVIL'),
     ))
     timestamp = models.DateTimeField(auto_now_add=True)
     successfull = models.BooleanField(default=False)
     amount = models.FloatField()
     raw_response = models.TextField()

     def __str__(self):
         return f"PAYMENT-{self.order}-{self.pk}"




class Cupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cupons')
    code = models.CharField(max_length=15)
    discount= models.IntegerField(default=0)
    discount_porcent= models.IntegerField(default=0)
    details = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    finished= models.DateTimeField()
    consumers=models.ManyToManyField(User, related_name='consumers', blank=True)
    orders=models.ManyToManyField(Order, blank=True)
    products=models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.code

def pre_save_merchant_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    if instance.pk is None:
        if instance.image:
            instance.resize(instance.image, (200, 200))
        if instance.banner:
            instance.resize(instance.banner, (700, 40))
        if instance.logo:
            instance.resize(instance.logo, (200, 200))
pre_save.connect(pre_save_merchant_receiver, sender=Merchant)


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
    if instance.pk is None and instance.image:
        instance.resize(instance.image, (380, 304))
pre_save.connect(pre_save_product_receiver, sender=Product)


def pre_safe_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    if instance.pk is None and instance.image:
        instance.resize(instance.image, (400, 400))
pre_save.connect(pre_safe_category_receiver, sender=Category)

