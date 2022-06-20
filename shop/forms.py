# from email.policy import default
# from itertools import product
from email.policy import default
from pyexpat import model
from django import forms
from django.forms import Select, Textarea, fields
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from pkg_resources import require
from ckeditor.fields import RichTextField

from .models import (
    Address,
    Brand,
    Category,
    Localidad,
    Merchant,
    Municipio,
    OrderItem, 
    ColorVariation,
    Pais, 
    Product,
    ProductImagesContent,
    Provincia,
    SizeVariation,
    Tag,
    Order,
    
)

User = get_user_model()    


class AddToCartForm(forms.ModelForm):
    
    colour = forms.ModelChoiceField(queryset=ColorVariation.objects.none(), label="Color", required=False)
    size = forms.ModelChoiceField(queryset=SizeVariation.objects.none(), label="Medida", required=False)
    quantity = forms.IntegerField(label="Cantidad", initial=1)
    class Meta:
        model = OrderItem
        fields = ['quantity', 'colour', 'size']

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        product = Product.objects.get(id=product_id)

        super().__init__(*args, **kwargs)

        if product.avialable_sizes.all():
            self.fields['size'].queryset = product.avialable_sizes.all()
        else:
            self.fields['size'].widget = forms.HiddenInput() #Oculta el campo

        if product.avialable_colours.all():
            self.fields['colour'].queryset = product.avialable_colours.all()
        else:
            self.fields['colour'].widget = forms.HiddenInput() #Oculta el campo
        # self.fields['colour'].queryset = product.avialable_colours.all()
        # self.fields['size']=self.hidden_fields()

  

class AddressForm(forms.Form):
    first_name=forms.CharField(label="Nombres", help_text="Agregar nombres")
    last_name=forms.CharField(label="Apellidos", help_text="Agregar apellidos")
    phone=forms.CharField(label="Teléfonos", max_length=11, help_text="Separar por ; si desea agregar más de un número")
    email=forms.CharField(label="Correo", help_text="Agregar correo electrónico válido")

    pais = forms.ModelChoiceField(
        queryset = Pais.objects.none(), widget=Select(attrs={'class':'select2'}), required=False
    )
    provincia = forms.ModelChoiceField(
        queryset= Provincia.objects.none(), widget=Select(attrs={'class':'select2'}), required=False
    )
    municipio = forms.ModelChoiceField(
        queryset= Municipio.objects.none(), widget=Select(attrs={'class':'select2'}), required=False
    )
    localidad = forms.ModelChoiceField(
        queryset= Localidad.objects.none(), widget=Select(attrs={'class':'select2'}), required=False
    )
 
    delivery_method = forms.ChoiceField(widget = forms.Select(), 
        choices = Order.DELIVERY_METHOD_CHOICES, initial=1, required = True,label="Entrega", help_text="Modifique el valor si desea recoger la orden en nuestro local",)
    
    address_line_1 = forms.CharField(label="Dirección de envio calle 1", help_text='Calle principal', required=False)
    address_line_2 = forms.CharField(label="Dirección de envio calle 2", help_text='Entre calles de la dirección',required=False)
    # localidad = forms.CharField(label="Localidad (barrio)", help_text="agregar localidad en que se ubica la dirección", required=False, error_messages="")
    numero = forms.CharField(label="Número de la casa", help_text="agregar el número de la casa (pasillo o edi.)", required=False, error_messages="")
    apt = forms.CharField(label="Número de apartamento", help_text="Solo en caso de Edif o pasillo", required=False, error_messages="")
    # delivery_method = forms.CharField(label="Entrega", help_text="Modifique el valor si desea recoger la orden en nuestro local", error_messages="")
    note=forms.CharField(required=False, help_text="Agregar información de interés para su pedido",widget=Textarea())

    # note=forms.CharField()

    class Meta:
        model = Address
        fields = ['first_name','last_name','phone','email','pais','provincia','municipio','localidad','delivery_method','address_line_1','address_line_2','localidad','numero','apt','note']

      
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        user = User.objects.get(id=user_id)
        super().__init__(*args, **kwargs)
        
        
        self.fields['pais'].queryset = Pais.objects.all()
        self.fields['provincia'].queryset = Provincia.objects.all()
        self.fields['municipio'].queryset = Municipio.objects.all()
        self.fields['localidad'].queryset = Localidad.objects.all()
        self.fields['first_name'].initial = user.profile.first_name
        self.fields['last_name'].initial = user.profile.last_name
        self.fields['phone'].initial = user.profile.phone
        self.fields['email'].initial = user.email
        self.fields['delivery_method'].initial = user.email
        try: 
            address_user = Address.objects.get(user=user)
       
            self.fields['pais'].initial = address_user.pais
            self.fields['provincia'].initial = address_user.provincia
            self.fields['municipio'].initial = address_user.municipio
            self.fields['address_line_1'].initial = address_user.address_line_1
            self.fields['address_line_2'].initial = address_user.address_line_2
            self.fields['localidad'].initial = address_user.localidad
            self.fields['numero'].initial = address_user.numero
         
        except ObjectDoesNotExist:
            print("No existe direccion del")

        # shipping_address_qs = Address.objects.filter(
        #     user = user,
        #     address_type='S'
        # )

        # billing_address_qs = Address.objects.filter(
        #     user = user,
        #     address_type='B'
        # )

        # self.fields['selected_shipping_address'].queryset = shipping_address_qs
        # self.fields['selected_billing_address'].queryset = billing_address_qs
        # self.fields['city'] = 'La Habana'


    # def clean(self):
    #     data = self.cleaned_data

        # selected_shipping_address = data.get('selected_shipping_address', None)
        # if selected_shipping_address is None:
        #     if not data.get('shipping_address_line_1', None):
        #         self.add_error("shipping_address_line_1", "Por favor complete este campo")
        #     if not data.get('shipping_address_line_2', None):
        #         self.add_error("shipping_address_line_2", "Por favor complete este campo")
        #     # if not data.get('shipping_zip_code', None):
        #         # self.add_error("shipping_zip_code", "Por favor complete este campo")
        #     if not data.get('shipping_city', None):
        #         self.add_error("shipping_city", "Por favor complete este campo")

        # selected_billing_address = data.get('selected_billing_address', None)
        # if selected_billing_address is None:
        #     if not data.get('billing_address_line_1', None):
        #         self.add_error("billing_address_line_1", "Por favor complete este campo")
        #     if not data.get('billing_address_line_2', None):
        #         self.add_error("billing_address_line_2", "Por favor complete este campo")
        #     # if not data.get('billing_zip_code', None):
        #         # self.add_error("billing_zip_code", "Por favor complete este campo")
        #     if not data.get('billing_city', None):
        #         self.add_error("billing_city", "Por favor complete este campo")
     







class AddProductBasicForm(forms.ModelForm):
    

    # category = forms.ModelMultipleChoiceField(label="Categorias", queryset=Category.objects.all(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    category = forms.ModelMultipleChoiceField(label="Categorias", queryset=Category.objects.all(), required=False)
    merchant = forms.ModelChoiceField(queryset = Merchant.objects.none(),label="Tienda", widget=Select(attrs={'class':'select2'}), required=False)
    brand = forms.ModelChoiceField(queryset = Brand.objects.none(), label="Marca", widget=Select(attrs={'class':'select2'}), required=False)
    # tag = forms.ModelMultipleChoiceField(label="Etiquetas", queryset=Tag.objects.all(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    product_images = forms.FileField(label="Galeria del producto",help_text="Agregar hasta 5 imagenes del producto", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    # avialable_colours = forms.ModelMultipleChoiceField(label="Colores", queryset=ColorVariation.objects.none(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    # avialable_sizes = forms.ModelMultipleChoiceField(label="Medidas", queryset=SizeVariation.objects.none(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    # related_products = forms.ModelMultipleChoiceField(label="Productos relacionados", queryset=Product.objects.none(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    title=forms.CharField(label="Nombre del producto", help_text="Agregar nombre descriptivo del producto")
    image=forms.ImageField(label="Imagen principal", help_text="Poner la imagen principal del producto")
    price=forms.IntegerField(label="Precio", help_text="Agregar precio del producto")
    stock=forms.IntegerField(label="Productos en stock", help_text="Agregar la cantidad de productos disponibles para la venta")
    old_price=forms.IntegerField(label="Precio anterior", help_text="Solo agregar si existe un precio anterior menor al actual")
    description=forms.Textarea()
    details=RichTextField()
    for_auction=forms.BooleanField(label="Producto para subasta", required=False, initial=False)

    class Meta:
        model = Product
        fields = ['category','merchant','title','image','product_images','price','stock','old_price','description','details','brand','for_auction']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        
        
        # self.fields['category'].queryset = Category.objects.all()
        self.fields['merchant'].queryset = Merchant.objects.filter(user=user)
        self.fields['brand'].queryset = Brand.objects.all()
        # self.fields['tag'].queryset = Tag.objects.all()
        self.fields['product_images'].queryset = ProductImagesContent.objects.filter(user=user)
        # self.fields['avialable_colours'].initial = ColorVariation.objects.all()
        # self.fields['avialable_sizes'].initial = SizeVariation.objects.all()
        # self.fields['related_products'].initial = Product.objects.all()
        


class AddDigitalProductForm(forms.ModelForm):
     # category = forms.ModelMultipleChoiceField(label="Categorias", queryset=Category.objects.all(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    category = forms.ModelMultipleChoiceField(label="Categorias", queryset=Category.objects.all(), required=False)
    merchant = forms.ModelChoiceField(queryset = Merchant.objects.none(),label="Tienda", widget=Select(attrs={'class':'select2'}), required=False)
    # tag = forms.ModelMultipleChoiceField(label="Etiquetas", queryset=Tag.objects.all(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    product_images = forms.FileField(label="Galeria del producto",help_text="Agregar hasta 5 imagenes del producto", widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    # related_products = forms.ModelMultipleChoiceField(label="Productos relacionados", queryset=Product.objects.none(),widget=Select(attrs={'class':'select2', 'multiple':'multiple'}), required=False)
    title=forms.CharField(label="Nombre del producto", help_text="Agregar nombre descriptivo del producto")
    image=forms.ImageField(label="Imagen principal", help_text="Poner la imagen principal del producto")
    price=forms.IntegerField(label="Precio", help_text="Agregar precio del producto")
    old_price=forms.IntegerField(label="Precio anterior", help_text="Solo agregar si existe un precio anterior menor al actual")
    description=forms.Textarea()
    details=RichTextField()
    
    content_file=forms.FileField(label="Archivo", help_text="Agregar archivo descargable maximo 5mb", required=False)
    content_url=forms.URLField(label="URL del contenido", help_text="Agrega la url del contenido a descargar", required=False)

  
    class Meta:
        model = Product
        fields = ['category','merchant','title','image','product_images','price','stock','old_price','description','details','content_file','content_url' ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        
        
        # self.fields['category'].queryset = Category.objects.all()
        self.fields['merchant'].queryset = Merchant.objects.filter(user=user)
        # self.fields['brand'].queryset = Brand.objects.all()
        # self.fields['tag'].queryset = Tag.objects.all()
        self.fields['product_images'].queryset = ProductImagesContent.objects.filter(user=user)
        # self.fields['avialable_colours'].initial = ColorVariation.objects.all()
        # self.fields['avialable_sizes'].initial = SizeVariation.objects.all()
        # self.fields['related_products'].initial = Product.objects.all()





class AddMerchanForm(forms.ModelForm):

    name=forms.CharField(label="Nombre de la Tienda")
    logo=forms.ImageField(label="Logo")
    image=forms.ImageField(label="Imagen principal")
    banner=forms.ImageField(label="Banner")
    phone=forms.CharField(label="Teléfono")
    description=RichTextField()
    address = forms.ModelChoiceField(queryset = Address.objects.none(),label="Dirección de la tienda", widget=Select(attrs={'class':'select2'}), required=False)
    public = forms.BooleanField(initial=True)

    class Meta:
        model = Merchant
        fields = ['name','logo','image','banner','phone','description','address','public']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        
        self.fields['address'].queryset = Address.objects.filter(user=user)
  

class PaymentDigitalProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['title','description','price']