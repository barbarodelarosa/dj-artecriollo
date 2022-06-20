import datetime
from itertools import product
import json
from utils.utils import costo_envio
from utils.enviar_emails import nueva_orden
from profile.models import Profile, UserLibrary
from django import template
from django.views import generic
from django.db.models import Q
from requests import request

import shop
from .utils import get_or_set_order_session, get_whishlist_session
from .models import Localidad, Merchant, Municipio, Product, OrderItem, Address, Payment, Order, Category, ProductImagesContent, WhishList
from .forms import AddDigitalProductForm, AddMerchanForm, AddProductBasicForm, AddToCartForm, AddressForm, PaymentDigitalProductForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from shop import enzona
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMessage



from shop import models


class CategoryDeatilView(generic.DetailView):
    model = Category
    template_name='shop/product_detail.html'


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'shop/category_list.html'


class CreateProductView(LoginRequiredMixin, generic.FormView):
    template_name='shop/create_product.html'
    form_class=AddProductBasicForm
    success_url="shop:create-product"



    def get_form_kwargs(self):
        kwargs = super(CreateProductView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        print(self.request.user)
        return kwargs

    def form_invalid(self, form: AddProductBasicForm) -> HttpResponse:
      
        return super().form_invalid(form)

    def form_valid(self, form):
     
        files_objs = []

        files = self.request.FILES.getlist('product_images')
        for file in files:
            file_instant = ProductImagesContent(file=file, user=self.request.user,)
            file_instant.save()
            files_objs.append(file_instant)


        categories = form.cleaned_data['category']
        # tag = form.cleaned_data['tag'],
    
        # avialable_colours = form.cleaned_data.get('avialable_colours')
        # avialable_sizes = form.cleaned_data.get('avialable_sizes')
        # related_products = form.cleaned_data.get('related_products')

        created = Product.objects.create(
            user = self.request.user,
            brand = form.cleaned_data.get('brand'),
            merchant = form.cleaned_data.get('merchant'),
            title = form.cleaned_data.get('title'),
            slug = form.cleaned_data.get('slug'),
            image = form.cleaned_data.get('image'),
            price = form.cleaned_data.get('price'),
            old_price = form.cleaned_data.get('old_price'),
            description = form.cleaned_data.get('description'),
            details = form.cleaned_data.get('details'),
            created = form.cleaned_data.get('created'),
            updated = form.cleaned_data.get('updated'),
            active = True,
            stock = form.cleaned_data.get('stock'),
            new = True,
            selling = False,
            digital = False,
            content_url = form.cleaned_data.get('content_url'),
            content_file = form.cleaned_data.get('content_file'),
            for_auction = False,
            selling_date = form.cleaned_data.get('selling_date'),
        )

        created.product_images.set(files_objs)
        created.category.set(categories)
        # created.tag.set(tag)
        # created.avialable_colours.set(avialable_colours)
        # created.avialable_sizes.set(avialable_sizes)
        # created.related_products.set(related_products)
        created.save()
        messages.info(self.request,"Producto agregado exitosamente")
        return super().form_valid(form)

    
class CreateDigitalProductView(LoginRequiredMixin, generic.FormView):
    template_name='shop/create_digital_product.html'
    form_class=AddDigitalProductForm
    success_url="admin"



    def get_form_kwargs(self):
        kwargs = super(CreateDigitalProductView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        print(self.request.user)
        return kwargs

    def form_invalid(self, form: AddDigitalProductForm) -> HttpResponse:
        return super().form_invalid(form)


    def form_valid(self, form):
     
        files_objs = []

        files = self.request.FILES.getlist('product_images')
        for file in files:
            file_instant = ProductImagesContent(file=file, user=self.request.user,)
            file_instant.save()
            files_objs.append(file_instant)

        

        print(form)
        categories = form.cleaned_data['category']
        content_file = form.cleaned_data['content_file']
        print(content_file)
        # tag = form.cleaned_data['tag'],
    
        # avialable_colours = form.cleaned_data.get('avialable_colours')
        # avialable_sizes = form.cleaned_data.get('avialable_sizes')
        # related_products = form.cleaned_data.get('related_products')

        created = Product.objects.create(
            user = self.request.user,
            brand = form.cleaned_data.get('brand'),
            merchant = form.cleaned_data.get('merchant'),
            title = form.cleaned_data.get('title'),
            slug = form.cleaned_data.get('slug'),
            image = form.cleaned_data.get('image'),
            price = form.cleaned_data.get('price'),
            old_price = form.cleaned_data.get('old_price'),
            description = form.cleaned_data.get('description'),
            details = form.cleaned_data.get('details'),
            created = form.cleaned_data.get('created'),
            updated = form.cleaned_data.get('updated'),
            active = True,
            stock = form.cleaned_data.get('stock'),
            new = True,
            selling = False,
            digital = True,
            content_url = form.cleaned_data.get('content_url'),
            content_file = form.cleaned_data.get('content_file'),
            for_auction = False,
            selling_date = form.cleaned_data.get('selling_date'),
        )

        created.product_images.set(files_objs)
        created.category.set(categories)
        # created.tag.set(tag)
        # created.avialable_colours.set(avialable_colours)
        # created.avialable_sizes.set(avialable_sizes)
        # created.related_products.set(related_products)
        created.save()
        messages.info(self.request,"Producto agregado exitosamente")
        return super().form_valid(form)

    
class CreateMerchantView(LoginRequiredMixin, generic.FormView):
    template_name='shop/create_merchant.html'
    form_class=AddMerchanForm
   

    def get_success_url(self):
        return reverse("shop:create-merchant")



    def get_form_kwargs(self):
        kwargs = super(CreateMerchantView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        print(self.request.user)
        return kwargs

    def form_invalid(self, form: AddMerchanForm) -> HttpResponse:
        return super().form_invalid(form)


    def form_valid(self, form):
     

        created = Merchant.objects.create(
            user = self.request.user,
            name = form.cleaned_data.get('name'),
            slug = form.cleaned_data.get('slug'),
            logo = form.cleaned_data.get('logo'),
            image = form.cleaned_data.get('image'),
            banner = form.cleaned_data.get('banner'),
            description = form.cleaned_data.get('description'),
            phone = form.cleaned_data.get('phone'),
            address = form.cleaned_data.get('address'),
            # status = form.cleaned_data.get('status'),
            public = form.cleaned_data.get('public'),
        )

        created.save()
        messages.info(self.request,"Tienda creada exitosamente, debe esperar a que ésta sea aprobada por los administradores")
        return super().form_valid(form)




class ProductListView(generic.ListView):
    template_name='shop/product_list.html'
    # paginate_by = 1
    
    def get_queryset(self):
        # qs = Product.objects.all()
        next = self.request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
        category = self.request.GET.get('slug', None)
        price_min = self.request.GET.get('price-min', None)
        price_max = self.request.GET.get('price-max', None)
        sort_by = self.request.GET.get('sort-by', None)
        show = self.request.GET.get('show', None)
        slug = self.kwargs['slug']


       
        if category or slug: 
            try:
                tag = Category.objects.get(slug=slug)
                if not price_min:
                    price_min = 0
                else:
                    price_min = float(price_min) 

                if not price_max:
                    price_max = 1000000    
                else:
                    price_max = float(price_max)
                price_min = price_min*100
                price_max = price_max*100
       
                if not sort_by:
                    sort_by = '-created'
                
                # print(tag.product_set.filter(Q(price__lte = price_max) & Q(price__gte = price_min)).order_by(sort_by)) #
                qs = tag.product_set.filter(aprobated=True, active=True, for_auction=False).filter(Q(price__lte = price_max) & Q(price__gte = price_min)).order_by(sort_by)
                
                # Q(secondary_categories__slug=category))
                paginator = Paginator(qs, 12)
                # object_list = object.page(page).object_list
                page_number = self.request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return page_obj
            except Category.DoesNotExist:
                return Product.objects.none()
        elif next:
            pass

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        parametros = self.request.GET.copy() #Obtiene todos los parametros de la url para despues enviarlos a la plantilla
        context.update({
            "categories": Category.objects.all(),
            "category_slug": self.request.GET.get('slug', None),
            "parametros": parametros
        })

        if (parametros.get('page') != None):
            del parametros['page']
        else:
            del parametros
        return context

class ProductDetailView(generic.FormView):
    template_name = 'shop/product_detail.html'
    form_class = AddToCartForm
    
    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs["slug"])

    def get_success_url(self):
        return reverse("shop:summary")

    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs["product_id"] = self.get_object().id
        return kwargs

    def form_valid(self, form):
      
        order = get_or_set_order_session(self.request)
        if not order.shipping:
            try:
                shipping_address = Address.objects.get(user=self.request.user)
                order = get_or_set_order_session(self.request)
                order.shhiping = shipping_address.localidad.shipping
                print("PRECIO SHIPPING",order.shhiping)
                order.save()
            except:
                pass
        product = self.get_object()

        item_filter = order.items.filter(
            product=product,
            colour=form.cleaned_data['colour'],
            size=form.cleaned_data['size']
        )

        if item_filter.exists():
            item = item_filter.first()
            # item.quantity += int(form.cleaned_data['quantity'])
            # item.save()
            quantity = int(form.cleaned_data['quantity'])
            print("item.quantity")
            print(quantity)
            if quantity <= product.stock:
                item.quantity += int(form.cleaned_data['quantity'])
                item.save()
                print("product.stock")
                print(product.stock)
                product.stock -= quantity
                product.save()
                print("product.stock")
                print(product.stock)
                item.save()
            else:
                # item.quantity -= int(form.cleaned_data['quantity'])
                # item.save()
                next = self.request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
                if item.quantity >0:
                    messages.info(self.request, f"No exite la cantidad de productos disponibles, ya usted tiene {item.quantity} producto(s) en carrito")
                else:
                    messages.info(self.request,"No exite la cantidad de productos disponibles")
                return redirect(next)
        else:


            quantity = int(form.cleaned_data['quantity'])
            print("item.quantity")
            print(quantity)
            if quantity <= product.stock:
          
                print("product.stock")
                print(product.stock)
                product.stock -= quantity
                product.save()
                print("product.stock")
                print(product.stock)
          
            else:
                # item.quantity -= int(form.cleaned_data['quantity'])
                # item.save()
                next = self.request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
            
                messages.info(self.request,"No exite la cantidad de productos disponibles")
                return redirect(next)


            new_item = form.save(commit=False)
            new_item.product = product
            new_item.order = order
            new_item.save()
        
        return super(ProductDetailView, self).form_valid(form)


    def get_context_data(self, **kwargs):

        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()
        
        
        return context


class CartView(generic.TemplateView):
    template_name = 'shop/cart.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context


class IncreaseQuantityView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        # product = get_object_or_404(Product, orderitem=order_item)

        # if product.stock >= 1:
        if order_item.product.stock > 0:
            order_item.quantity += 1
        
            order_item.product.stock -= 1
            order_item.product.save()
            print("order_item.product.stock")
            print(order_item.product.stock)
                # product.stock -= 1
                # product.save()
            order_item.save()
        else:
            messages.info(self.request, "No quedan productos disponibles por el momento")            

        # else:
            # order_item.save()
        return redirect("shop:summary")


class DecreaseQuantityView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        # product = get_object_or_404(Product, orderitem=order_item)

        # order_item.quantity <= 1:
            # product.stock -= 1
            # product.save()
        order_item.delete()

        # else:
        order_item.quantity -= 1
  
        order_item.product.stock += 1
        order_item.product.save()
    
            # product.stock += 1
            # product.save()
        order_item.save()
        return redirect("shop:summary")


class RemoveFromCartView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        print("order_item.product.stock")
        print(order_item.product.stock)
        order_item.product.stock += order_item.quantity
        order_item.product.save()
        print("order_item.product.stock")
        print(order_item.product.stock)
   
        order_item.delete()
        next = self.request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
        return redirect(next)



class CheckoutView(LoginRequiredMixin, generic.FormView):
    template_name = 'shop/checkout.html'
    form_class = AddressForm

    def get_success_url(self):
        payment_method = self.request.POST.get('payment_method')
       
        self.request.session['payment_method']=payment_method
        print("PAYMENT METHOD************************",payment_method)
        if payment_method == "efectivo":
            print("REDIREC TO CASH")
            return reverse("shop:confirm-order")
        elif payment_method=="enzona":
            print("REDIREC TOENZONA")
            return reverse("shop:payment-enzona")
        messages.error(request, "Hubo un error al procesa al metodo de pago")
        next = self.request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual

        return redirect(next)

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        connect = enzona.test_connect()
        payment_method = self.request.POST.get('payment')


        if payment_method == 'efectivo':
            items = []
            

            for item in order.items.all():
    
                temp_item ={}

                temp_item['name']=item.product.title
                temp_item['description']=item.product.description
                temp_item['quantity']=item.quantity
                temp_item['tax']=f'{item.get_tax()}'
                temp_item['price']=f'{item.product.get_price()}'
                # temp_item['price']=f'{item.get_total_item_price()}'
                items.append(temp_item)




            order.payment_method='EFECTIVO'
            order.save()
            self.request.session['payment_method']='efectivo'
        



       
        if payment_method=="enzona":

            try:
                error = connect.get('error')
                if error:
                    messages.error(self.request, "No se detecta conexión con ENZONA :( , por favor intente nuevamente, de continuar la situación seleccione la opción de PAGO CON EFECTIVO o contactar con el administrador")
                    return HttpResponseRedirect(redirect_to=f'{self.request.build_absolute_uri()}')
            except:
                pass
        # selected_shipping_address = form.cleaned_data.get('selected_shipping_address')
        # selected_billing_address = form.cleaned_data.get('selected_billing_address')

        # if selected_shipping_address:
            # order.shipping_address = selected_shipping_address
        # else:
        #     address = Address.objects.create(
        #         address_type = 'S',
        #         user = self.request.user,
        #         address_line_1=form.cleaned_data['shipping_address_line_1'],
        #         address_line_2=form.cleaned_data['shipping_address_line_2'],
        #         # zip_code=form.cleaned_data['shipping_zip_code'],
        #         city=form.cleaned_data['shipping_city'],
        #     )
        #     order.shipping_address = address

        # if selected_billing_address:
        #     order.billing_address = selected_billing_address
        # else:
        #     address = Address.objects.create(
        #         address_type = 'B',
        #         user = self.request.user,
        #         address_line_1=form.cleaned_data['billing_address_line_1'],
        #         address_line_2=form.cleaned_data['billing_address_line_2'],
        #         # zip_code=form.cleaned_data['billing_zip_code'],
        #         city=form.cleaned_data['billing_city'],
        #     )
        #     order.billing_address = address
        # address_exist = Address.objects.get(user=self.request.user).exist()
        # if Address.objects.filter(user=self.request.user).exist():
        #     Address.objects.get(user=self.request.user).delete()
        


        from django.core.exceptions import ObjectDoesNotExist
        try:
            address_exist = Address.objects.get(user=self.request.user)
            address_exist.delete()

    
        except ObjectDoesNotExist:
            print("Either the blog or entry doesn't exist.")
        address = Address.objects.create(
            address_type = 'P',
            user = self.request.user,
            address_line_1=form.cleaned_data['address_line_1'],
            address_line_2=form.cleaned_data['address_line_2'],
            # zip_code=form.cleaned_data['billing_zip_code'],
            # city=form.cleaned_data['city'],
            pais = form.cleaned_data['pais'],
            provincia = form.cleaned_data['provincia'],
            municipio = form.cleaned_data['municipio'],
            localidad = form.cleaned_data['localidad'],
            
            numero = form.cleaned_data['numero'],
            apt = form.cleaned_data['apt'],
        
            
            )
        # order.billing_address = address
        order.shipping_address = address
        order.first_name = form.cleaned_data.get('first_name')       
        order.last_name = form.cleaned_data.get('last_name')
        order.phone = form.cleaned_data.get('phone')
        order.email = form.cleaned_data.get('email')
        order.status = 'EN PREPARACIÓN'
        order.note = form.cleaned_data.get('note')
        order.save()

        # order_object = Order.objects.get(user=self.request.user)
        
        # print(order_object)
        print("ORDERRRRRR",order)
        messages.info(
            self.request, "Se ha agregado la dirección")
        # return super(CheckoutView, self).form_valid(form)

        # next = self.request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
        # return redirect(next) #PARA NO SALIR DE LA PAGINA

        return super(CheckoutView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
       
        context['order'] = get_or_set_order_session(self.request)
        return context



def actualizar_costo_mensajeria(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    order = get_or_set_order_session(request)
    if is_ajax:
        if request.method=="POST":
            data = json.load(request)
            payload = data.get('payload')
            localidad = payload['localidad']
            delivery_method  = payload['delivery_method']
            
            address, created = Address.objects.get_or_create(user=request.user)
            localidad_get = Localidad.objects.get(name=localidad)
            print("MUNICIPIO",localidad)
            if created:
                address = Address.objects.get(user=request.user)
            address.localidad = localidad_get
            address.save()
            # if delivery_method:
            if delivery_method == "DOMICILIO":
                print("DELIVERY",delivery_method)
                order.shipping = localidad_get.shipping
                print("DELIVERY",order.shipping)
                costo_envio_en_cup = "{:.2f}".format(order.shipping / 100)
                messages.info(request, f"Usted a seleccionado la localidad de: {address.localidad} y tendra un costo por envio de: {costo_envio_en_cup} cup")
            else:
                print("MUNICIPIO",localidad)

                order.shipping = 0
                print("MUNICIPIO",order.shipping)
                messages.info(request, "Usted a seleccionado recogida local para su pedido y no tendrá costo adicional por envio. ")
            order.save()
        
            next = request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
            return redirect(next)
    else:
        return HttpResponseBadRequest('Invalid request')
    

    # order.shipping_address = address
class PaymentView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'shop/payment.html'

    # def get_context_data(self, **kwargs):
    #     context = super(PaymentView, self).get_context_data(**kwargs)
    #     context["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
    #     context['order'] = get_or_set_order_session(self.request)
    #     context['CALLBACK_URL']= self.request.build_absolute_uri(reverse("cart:thank-you"))
    #     return context





class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'order.html'
    queryset = Order.objects.all()
    context_object_name = 'order'
 


# class ConfirmEnzonaPaymentView(generic.View):
class ConfirmEnzonaPaymentView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'shop/confirm_enzona_payment.html'
    def get(self, request, *args, **kwargs):
    # def get_context_data(self, *args, **kwargs):
        context = super(ConfirmEnzonaPaymentView, self).get_context_data(**kwargs)
        order = get_or_set_order_session(self.request)
        items = []
        

        for item in order.items.all():
   
            temp_item ={}

            temp_item['name']=item.product.title
            temp_item['description']=item.product.description
            temp_item['quantity']=item.quantity
            temp_item['tax']=f'{item.get_tax()}'
            temp_item['price']=f'{item.product.get_price()}'
            # temp_item['price']=f'{item.get_total_item_price()}'
            items.append(temp_item)
   
        amount = {
            "total": "2.00",
            "details": {
            "shipping": "0.00",
            "tax": "0.00",
            "discount": "0.00",
            "tip": "0.00"
            }
        }
        
        amount['total']=f'{order.get_total()}' #OK
        amount['details']['shipping']=f'{order.get_total_shipping()}'
        amount['details']['tax']=f'{order.get_total_tax()}'
        amount['details']['discount']=f'{order.get_total_discount()}'

        print("items")
        print(items)
        print("amount")
        print(amount)
      
 ###################### BLOQUE DE CONSULTA A ENZONA #######################
        cancel_url=f'https://{self.request.get_host()}/shop/checkout/'
        return_url=f'https://{self.request.get_host()}/shop/confirm-order/'
        print(cancel_url)
        print(return_url)
        resp_enzona = enzona.post_payments(
            description=f'Orden de pago - {order.id}',
            currency="CUP",
            amount=amount,
            items=items,
            cancel_url=f'{cancel_url}',
            return_url=f'{return_url}'
            )
        print("resp_enzona.json()")
        # print(resp_enzona.json())
        
        if resp_enzona.status_code == 200:
      
            resp_content = resp_enzona.json()
            links_resp = resp_content['links']
            url_confirm = links_resp[0]
            context['url_confirm'] = url_confirm
            self.request.session['payment_method']='enzona'
            return redirect(to=url_confirm['href']) #Redirecciona a enzona para confirmar el pago
        else:
            print("resp_enzona.status_code")
            print(resp_enzona.status_code)
            print(resp_enzona.status_code)
            
     
        context['resp_enzona'] = resp_enzona.json()

 ###################### FIN BLOQUE DE CONSULTA A ENZONA #######################

        order.payment_method='ENZONA'
        order.save()
        context['order'] = get_or_set_order_session(self.request)



        # print('=====================================')
        # print(order.items.all())
        # print('=====================================')
    

        # context['CALLBACK_URL']= self.request.build_absolute_uri(reverse("shop:thank-you"))
        return context

























class ConfirmOrderView(LoginRequiredMixin, generic.View): #Confirma el pago realizado por el usuario
    def get(self, request, *args, **kwargs):
        digital_product=None
        payment_method=None
        try:
            payment_method = request.session['payment_method']
           
        except:
            pass

        if payment_method == 'efectivo':
            order = get_or_set_order_session(request)
            amount=order.get_total()
            payment = Payment.objects.create(
                order=order,
                successfull=True,
                # raw_response = "Respuesta de prueba",
                # raw_response = json.dumps(body),
                # amount = float(body["purchase_units"][0]["amount"]["value"]),
                amount = amount,
                payment_method='EFECTIVO'
            )
            order.ordered = True
            order.ordered_date = datetime.datetime.now()

            for item in order.items.all(): #Funcion para agregar al producto la fecha en que fue vendido   
                item.product.selling_date = datetime.datetime.now()
                item.product.save()

            order.save()
            messages.info(request, message="Se ha realizado correctamente su pedido")
            nueva_orden(request, order, "PRODUCTO FISICO")
            try: 
                ref_profile = request.session['ref_profile'] #Recibir referencia y agregarla a la cuenta del usuario
                profile = Profile.objects.get(id=ref_profile)
                profile.recommended_products.add(order)
                profile.save()
                del request.session['ref_profile'] #Elimina la referencia de usuario
            except:
                pass
            
    
            del request.session['payment_method'] #Elimina el metodo de pago
            return redirect(to="shop:thankyou")


#************************ ENZONA**********************

        if payment_method == 'enzona':
            try:
                digital_product = request.session['digital_product']
                        
            except:
                pass

            transaction_uuid = request.GET['transaction_uuid']
            user_uuid = request.GET['user_uuid']
            print("DIGITAL PRODUCT EN CONFIRM ORDER", digital_product)
            if not digital_product:
                order = get_or_set_order_session(request)
            
                payment = Payment.objects.create(
                    order=order,
                    successfull=True,
                    # raw_response = "Respuesta de prueba",
                    # raw_response = json.dumps(body),
                    # amount = float(body["purchase_units"][0]["amount"]["value"]),
                    amount = float(33.56),
                    payment_method='ENZONA'
                )
                order.ordered = True
                order.ordered_date = datetime.datetime.now()

                for item in order.items.all(): #Funcion para agregar al producto la fecha en que fue vendido   
                    item.product.selling_date = datetime.datetime.now()
                    item.product.save()

                order.save()
                messages.info(request, message="Se ha realizado Correctamente el pago")
                nueva_orden(request, order, "PRODUCTO FISICO")

                try: 
                    ref_profile = request.session['ref_profile'] #Recibir referencia y agregarla a la cuenta del usuario
                    profile = Profile.objects.get(id=ref_profile)
                    profile.recommended_products.add(order)
                    profile.save()
                    del request.session['ref_profile'] #Elimina la referencia de usuario
                except:
                    pass

        
            else:
                #*******************************************************
                # Logica para agregar el producto digital a la libreria#
                #*******************************************************
                user_library = UserLibrary.objects.get(user=request.user)
                product = Product.objects.get(id=digital_product)
                user_library.products.add(product)
                user_library.save()
                messages.success(self.request, "Se ha agregado el producto a su librería para descarga")
                try: 
                    ref_profile = request.session['ref_profile'] #Recibir referencia y agregarla a la cuenta del usuario
                    profile = Profile.objects.get(id=ref_profile)
                    profile.recommended_digital_products.add(product)
                    profile.save() 
                    del request.session['ref_profile'] #Elimina la referencia de usuario
                except:
                    pass
                
                nueva_orden(request, product,'PRODUCTO DIGITAL')
                # return redirect(to="shop:thankyou")

                # UserLibrary
            



            confirm = enzona.confirm_payment_orders(transaction_uuid)

            return redirect(to="shop:thankyou")


class ThankYouView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'shop/thanks.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ThankYouView, self).get_context_data(**kwargs)
        context["prueba"] = "Prueba"
        try:
            request.session['digital_product']
            messages.info(request, message="Se ha realizado Correctamente el pago y el producto se ha agregado a su libreria de descargas")
            del  request.session['digital_product']
        except:
            pass
        return context



class WhishlistView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'shop/whishlist_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(WhishlistView, self).get_context_data(**kwargs)
        context["prueba"] = "Prueba"
        context["whishlist"] = get_whishlist_session(self.request)
        print("GET DATA WHISH")
        return context

# class AddOrRemoveToWhishlist(generic.View):
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         whishlist = WhishList.objects.get_or_create(user=user)
        
#         # order_item = get_object_or_create(OrderItem, id=kwargs['pk'])
#         print(whishlist)
#         # order_item.delete()
#         next = self.request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
#         return redirect(next)



# class DecreaseQuantityView(generic.View):
#     def get(self, request, *args, **kwargs):
#         order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
#         product = get_object_or_404(Product, orderitem=order_item)

#         if order_item.quantity <= 1:
#             product.stock -= 1
#             product.save()
#             order_item.delete()

#         else:
#             order_item.quantity -= 1
#             product.stock += 1
#             product.save()
#             order_item.save()
#         return redirect("shop:summary")


# class RemoveFromCartView(generic.View):
#     def get(self, request, *args, **kwargs):
#         order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
#         order_item.delete()
#         return redirect("shop:summary")

def addToCart(request,product_id):
    # user=request.user
    product = get_object_or_404(Product, id=product_id)
    order = get_or_set_order_session(request)
    if request.method=="POST":
        form = AddToCartForm(request.POST, 
        product_id=product_id)
      
        if form.is_valid():
           
            item_filter = order.items.filter(
            product=product,
            # colour=form.cleaned_data['colour'],
            # size=form.cleaned_data['size']
            )
            quantity=int(form.cleaned_data['quantity'])

            if item_filter.exists():
                if product.stock > 0:
                    item = item_filter.first()
                    item.quantity += quantity
                    item.save()
                    product.stock -= 1
                    product.save()
                    messages.success(request, f'{quantity} Producto{"s" if quantity>1 else ""} agregado al carrito')
                else:
                    messages.info(request, "No quedan productos disponibles")
            else:
                if product.stock > 0:
                    new_item = form.save(commit=False)
                    product.stock -= 1
                    product.save()
                    new_item.product = product
                    new_item.order = order
                    new_item.save()
                    messages.success(request, f'{quantity} Producto{"s" if quantity>1 else ""} agregado al carrito')
                else:
                    messages.info(request, "No quedan productos disponibles")
        
            
    next = request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
    return redirect(next)







class EnzonaPaymentDigitalProductView(LoginRequiredMixin, generic.TemplateView):

    # template_name = 'shop/confirm_enzona_payment.html'
    def get(self, request, *args, **kwargs):
        digital_product=request.session["digital_product"]
        product = Product.objects.get(pk=digital_product)
        return HttpResponseRedirect(reverse('shop:product-detail', kwargs={'category':product.category.first().slug, 'slug':product.slug}) )



    def post(self, request, *args, **kwargs):
        if request.method=="POST":
            form = PaymentDigitalProductForm(request.POST)
            print(form)
            if form.is_valid():
                name = form.cleaned_data.get("title")
                description = form.cleaned_data.get("description")
                price = form.cleaned_data.get("price")
            
                new_format_price = "{0:.2f}".format(price / 100)
                context = super(EnzonaPaymentDigitalProductView, self).get_context_data(**kwargs)
                
        
                items = []
                temp_item = {
                'name': name, #OJO ---> Los nombres no pueden tener caracteres especiales porque da error
                'description': description,
                'quantity': 1,
                'price': new_format_price,
                'tax': '0.00'
                }
                items.append(temp_item)
         
                amount = {
                    "total": new_format_price,
                    "details": {
                    "shipping": "0.00",
                    "tax": "0.00",
                    "discount": "0.00",
                    "tip": "0.00"
                    }
                }
             
         
                request.session["digital_product"]=kwargs['pk']
            
 ###################### BLOQUE DE CONSULTA A ENZONA #######################
             
                resp_enzona = enzona.post_payments(
                    description="description",
                    currency="CUP",
                    amount=amount,
                    items=items,
                    # cancel_url=f'http://{request.get_host()}/shop/', #OK
                    cancel_url=f'{request.build_absolute_uri()}', #OK
                    return_url=f'https://{request.get_host()}/shop/confirm-order/' #OK
                    )
            
                if resp_enzona.status_code == 200:
                   
                    resp_content = resp_enzona.json()
                    links_resp = resp_content['links']
                    url_confirm = links_resp[0]
                    context['url_confirm'] = url_confirm
                    # guardar valores en session para desdupes de confirmado el pago utilizarlos y eliminarlos
                    request.session['payment_method']='enzona'
                    return redirect(to=url_confirm['href']) #Redirecciona a enzona para confirmar el pago
                else:
                    pass
            
                context['resp_enzona'] = resp_enzona.json()

 ###################### FIN BLOQUE DE CONSULTA A ENZONA #######################

        # order.payment_method='ENZONA'
        # order.save()
        context['order'] = get_or_set_order_session(self.request)
        # print('=====================================')
        # print(order.items.all())
        # print('=====================================')
    

        # context['CALLBACK_URL']= self.request.build_absolute_uri(reverse("shop:thank-you"))
        return context

















"""
****************************************************************************
****************************************************************************
****************************************************************************
****************************************************************************
****************************************************************************
****************************************************************************
****************************************************************************
****************************************************************************
****************************************************************************
"""




# class ConfirmCashPaymentView(LoginRequiredMixin, generic.TemplateView):

#     template_name = 'shop/confirm_cash_payment.html'
#     # def get(self, request, *args, **kwargs):
#     def get_context_data(self, *args, **kwargs):
#         context = super(ConfirmCashPaymentView, self).get_context_data(**kwargs)
#         order = get_or_set_order_session(self.request)
#         items = []
        

#         for item in order.items.all():
   
#             temp_item ={}

#             temp_item['name']=item.product.title
#             temp_item['description']=item.product.description
#             temp_item['quantity']=item.quantity
#             temp_item['tax']=f'{item.get_tax()}'
#             temp_item['price']=f'{item.product.get_price()}'
#             # temp_item['price']=f'{item.get_total_item_price()}'
#             items.append(temp_item)




#         order.payment_method='EFECTIVO'
#         order.save()
#         self.request.session['payment_method']='efectivo'
#         context['order'] = get_or_set_order_session(self.request)
       
#         context['CALLBACK_URL']= self.request.build_absolute_uri(reverse("shop:thankyou"))
#         return context






