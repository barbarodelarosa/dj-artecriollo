from django.db import models


from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify




def user_directory_path(instance, filename):
    # This file will be uploaded to MEDIA_ROOT/the user{id}/thefile
    return 'user_{0}/product_{1}'.format(instance.user.username, filename)

class ProductImagesContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner', blank=True, null=True)
    file = models.FileField(upload_to= user_directory_path)
    posted = models.DateTimeField(auto_now_add=True)

   

User = get_user_model()



class Category(models.Model):
    image = models.ImageField(upload_to="image/category", blank=True, null=True) 
    name  = models.CharField(max_length=100)
    slug  = models.SlugField(unique=True)
    active= models.BooleanField(default=True)


    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

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
        super(Category, self).save(*args, **kwargs)


    def __str__(self):
        return self.name





  
class Address(models.Model):
    ADDRESS_CHOICES = (
        ('B', 'Billing'),
        ('S', 'Shipping'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=10)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line_1}, {self.address_line_1}, {self.city}, {self.zip_code}"

    class Meta:
        verbose_name_plural = 'Addresses'


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


class Product(models.Model):
    category = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    tag = models.ManyToManyField(Tag)
    title = models.CharField(max_length=150)
    product_images = models.ManyToManyField(ProductImagesContent, blank=True, related_name='images_product')
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='product_image')
    price = models.IntegerField(default=0)
    old_price = models.IntegerField(default=0)
    description = models.TextField()
    details = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    avialable_colours = models.ManyToManyField(ColorVariation)
    avialable_sizes = models.ManyToManyField(SizeVariation)
    stock = models.PositiveIntegerField(default=0)
    related_products = models.ManyToManyField('self', blank=True)
    
    
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

class WhishList(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    order = models.ForeignKey("Order", related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    colour = models.ForeignKey(ColorVariation, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVariation, on_delete=models.CASCADE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    shipping = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, blank=True, null=True)
    pay_status = models.CharField(max_length=15, choices=PAY_STATUS_CHOICES, blank=True, null=True)


    billing_address = models.ForeignKey(
        Address, related_name='billing_address', blank=True, null=True, on_delete=models.SET_NULL
    )
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

    def get_total_shipping(self):
        return "{0:.2f}".format(self.shipping / 100)

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
        discount = discount + self.discount
        print('discount')
        print(discount)
        subtotal = subtotal + tax + self.shipping - discount
        return subtotal

    def get_total(self):
        total = self.get_raw_total()
  
        return "{0:.2f}".format(total / 100)


class Payment(models.Model):
     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
     payment_method = models.CharField(max_length=20, choices=(
         ('Paypal', 'Paypal'),
         ('ENZONA', 'ENZONA'),
     ))
     timestamp = models.DateTimeField(auto_now_add=True)
     successfull = models.BooleanField(default=False)
     amount = models.FloatField()
     raw_response = models.TextField()

     def __str__(self):
         return f"PAYMENT-{self.order}-{self.pk}"


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(pre_save_product_receiver, sender=Product)