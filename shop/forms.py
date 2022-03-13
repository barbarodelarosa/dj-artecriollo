# from cProfile import label
from email.policy import default
from itertools import product
from django import forms
from django.forms import Select, Textarea, fields
from django.contrib.auth import get_user_model

from .models import (
    Address,
    Municipio,
    OrderItem, 
    ColorVariation,
    Pais, 
    Product,
    Provincia,
    SizeVariation,
    
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
    phone=forms.CharField(label="Teléfonos", help_text="Separar por ; si desea agregar más de un número")
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
    address_line_1 = forms.CharField(label="Dirección de envio calle 1", help_text='Calle principal', required=False)
    address_line_2 = forms.CharField(label="Dirección de envio calle 2", help_text='Entre calles de la dirección',required=False)
    localidad = forms.CharField(label="Localidad (barrio)", help_text="agregar localidad en que se ubica la dirección", required=False, error_messages="")
    numero = forms.CharField(label="Número de la casa", help_text="agregar el número de la casa (pasillo o edi.)", required=False, error_messages="")
    apt = forms.CharField(label="Número de apartamento", help_text="Solo en caso de Edif o pasillo", required=False, error_messages="")

    note=forms.CharField(required=False, help_text="Agregar información de interés para su pedido",widget=Textarea())

    # note=forms.CharField()

    class Meta:
        model = Address
        fields = ['first_name','last_name','phone','email','pais','provincia','municipio','address_line_1','address_line_2','localidad','numero','apt','note']

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        user = User.objects.get(id=user_id)
        super().__init__(*args, **kwargs)
        address_user = Address.objects.get(user=user)

        self.fields['pais'].queryset = Pais.objects.all()
        self.fields['provincia'].queryset = Provincia.objects.all()
        self.fields['municipio'].queryset = Municipio.objects.all()
        self.fields['first_name'].initial = user.profile.first_name
        self.fields['last_name'].initial = user.profile.last_name
        self.fields['phone'].initial = user.profile.phone
        self.fields['email'].initial = user.email
        self.fields['pais'].initial = address_user.pais
        self.fields['provincia'].initial = address_user.provincia
        self.fields['municipio'].initial = address_user.municipio
        self.fields['address_line_1'].initial = address_user.address_line_1
        self.fields['address_line_2'].initial = address_user.address_line_2
        self.fields['localidad'].initial = address_user.localidad
        self.fields['numero'].initial = address_user.numero
        self.fields['apt'].initial = address_user.apt

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
     