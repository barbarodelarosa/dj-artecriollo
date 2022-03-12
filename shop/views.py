import datetime
from itertools import product
import json
from django import template
from django.views import generic
from django.db.models import Q

import shop
from .utils import get_or_set_order_session, get_whishlist_session
from .models import Product, OrderItem, Address, Payment, Order, Category, WhishList
from .forms import AddToCartForm, AddressForm
from django.shortcuts import get_object_or_404, reverse, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from shop import enzona
from django.urls import reverse
from django.core.paginator import Paginator


from shop import models


class CategoryDeatilView(generic.DetailView):
    model = Category
    template_name='shop/product_detail.html'


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'shop/category_list.html'




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
                print("LATEST")
                if not sort_by:
                    sort_by = '-created'
                
                # print(tag.product_set.filter(Q(price__lte = price_max) & Q(price__gte = price_min)).order_by(sort_by)) #
                qs = tag.product_set.filter(Q(price__lte = price_max) & Q(price__gte = price_min)).order_by(sort_by)
                
                # Q(secondary_categories__slug=category))
                paginator = Paginator(qs, 2)
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


class IncreaseQuantityView(generic.View):
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


class DecreaseQuantityView(generic.View):
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


class RemoveFromCartView(generic.View):
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
        # return reverse("shop:payment-enzona")
        next = self.request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual

        return redirect(next)

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
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
        # from django.core.exceptions import ObjectDoesNotExist
        # try:
        address_exist = Address.objects.get(user=self.request.user)
        address_exist.delete()

    
        # except ObjectDoesNotExist:
        #     print("Either the blog or entry doesn't exist.")
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
        order.billing_address = address
        order.shipping_address = address
        order.first_name = form.cleaned_data.get('first_name')       
        order.last_name = form.cleaned_data.get('last_name')
        order.phone = form.cleaned_data.get('phone')
        order.email = form.cleaned_data.get('email')

        order.note = form.cleaned_data.get('note')
        order.save()
        order_object = Order.objects.get(user=self.request.user)
        
        print(order_object)
        messages.info(
            self.request, "You have successfully added your addresses")
        # return super(CheckoutView, self).form_valid(form)
        next = self.request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual

        return redirect(next)

        # return super(CheckoutView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        
        context['order'] = get_or_set_order_session(self.request)
        return context


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
    # def get(self, request, *args, **kwargs):
    def get_context_data(self, *args, **kwargs):
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
 
 ###################### BLOQUE DE CONSULTA A ENZONA #######################
        resp_enzona = enzona.post_payments(
            description="Probando agregar al diccionario",
            currency="CUP",
            amount=amount,
            items=items,
            cancel_url="http://127.0.0.1:8000/shop/",
            return_url="http://127.0.0.1:8000/shop/confirm-order/"
            )
        print("resp_enzona.json()")
        print(resp_enzona.json())
        if resp_enzona.status_code == 200:
            resp_content = resp_enzona.json()
            links_resp = resp_content['links']
            url_confirm = links_resp[0]
            context['url_confirm'] = url_confirm
            print(resp_content)
            # return redirect(to=url_confirm['href'])
        else:
            print(resp_enzona.status_code)
            
     
        context['resp_enzona'] = resp_enzona.json()

 ###################### FIN BLOQUE DE CONSULTA A ENZONA #######################

        order.payment_method='ENZONA'
        order.save()
        context['order'] = get_or_set_order_session(self.request)
        # print('=====================================')
        # print(order.items.all())
        # print('=====================================')
    

        # context['CALLBACK_URL']= self.request.build_absolute_uri(reverse("cart:thank-you"))
        return context






class ConfirmCashPaymentView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'shop/confirm_cash_payment.html'
    # def get(self, request, *args, **kwargs):
    def get_context_data(self, *args, **kwargs):
        context = super(ConfirmCashPaymentView, self).get_context_data(**kwargs)
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
 
        # resp_enzona = enzona.post_payments(
        #     description="Probando agregar al diccionario",
        #     currency="CUP",
        #     amount=amount,
        #     items=items,
        #     cancel_url="http://127.0.0.1:8000/shop/",
        #     return_url="http://127.0.0.1:8000/shop/confirm-order/"
        #     )
        # print("resp_enzona.json()")
        # print(resp_enzona.json())
        # if resp_enzona.status_code == 200:
        #     resp_content = resp_enzona.json()
        #     links_resp = resp_content['links']
        #     url_confirm = links_resp[0]
        #     context['url_confirm'] = url_confirm
        #     print(resp_content)
        #     # return redirect(to=url_confirm['href'])
        # else:
        #     print(resp_enzona.status_code)
            
     
        # context['resp_enzona'] = resp_enzona.json()

        order.payment_method='EFECTIVO'
        order.save()
        context['order'] = get_or_set_order_session(self.request)
    
        # print('=====================================')
        # print(order.items.all())
        # print('=====================================')
    

        # context['CALLBACK_URL']= self.request.build_absolute_uri(reverse("cart:thank-you"))
        return context




























class ConfirmOrderView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        transaction_uuid = request.GET['transaction_uuid']
        user_uuid = request.GET['user_uuid']
        print("user_uuid")
        print(user_uuid)
        print("transaction_uuid")
        print(transaction_uuid)
        # print(request.body)
        # body = json.loads(request.body)
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
        order.ordered_date = datetime.date.today()

        for item in order.items.all(): #Funcion para agregar al producto la fecha en que fue vendido   
            item.product.selling_date = datetime.datetime.now()
            item.product.save()

        order.save()
        messages.info(request, message="Se ha realizado Correctamente el pago")

        # return JsonResponse({"data": "Success"})
        confirm = enzona.confirm_payment_orders(transaction_uuid)
        print("confirm")
        print(confirm)
        return redirect(to="shop:thankyou")


class ThankYouView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'shop/thanks.html'
    


# CartView
# ProductListView
# ProductDetailView
# IncreaseQuantityView
# DecreaseQuantityView
# RemoveFromCartView
# CheckoutView
# PaymentView
# ConfirmEnzonaPaymentView



class WhishlistView(generic.TemplateView):
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
            if item_filter.exists():
                if product.stock > 0:
                    item = item_filter.first()
                    item.quantity += int(form.cleaned_data['quantity'])
                    item.save()
                    product.stock -= 1
                    product.save()
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
                else:
                    messages.info(request, "No quedan productos disponibles")
        
            
    next = request.META.get('HTTP_REFERER', None) or '/'  #Obtiene la url actual
    return redirect(next)