from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart,CartItem,Wishlist
from accounts.models import CustomUser,BillingAddress
from store.models import Product,ProductVariant,Color
from accounts.models import *
from orders.models import *
from django.contrib.auth.decorators import login_required

import json
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse
from accounts.forms import BillingAddressForm
from accounts.views import *


# Create your views here.

def add_to_cart(request):  
        id = request.GET['productid']
        print(id)
        user = request.user if request.user.is_authenticated else None
        cart,_= Cart.objects.get_or_create(user=user)
        print(user)
        product =Product.objects.get(pk=id)      
        price = request.GET['selectedprice']
        color =request.GET['selectedcolor']
       
        print(price)
        print(color)
        
       
       
        color_id = Color.objects.filter(name=color).values_list('pk', flat=True).first()
        print(color_id)
        variant = ProductVariant.objects.get(product_name_id=id,color_id=color_id)
        print(variant)
    
        if variant:
            try:
                if CartItem.objects.get(user=user,cart=cart,product=product,product_variant=variant):
                   cart_item = CartItem.objects.get(user=user,cart=cart,product=product,product_variant=variant)
                   print("there is an item")
                   cart_item.quantity = cart_item.quantity + 1
                    
                   cart_item.save()
                
            except :
                a=CartItem.objects.create(user=user,cart=cart,product=product,product_variant=variant,quantity=1)
                print(a)
            
            


            return JsonResponse({'status':400,"message":"added"})

def delete_cart_item(request,id):
    cart_item = get_object_or_404(CartItem, pk=id)
    cart_item.delete()
    return redirect('cart')



@login_required(login_url='signin')
def cart(request):
    # user = request.user if request.user.is_authenticated else None
    user = request.user
    try:
        if user:
          cart,_ = Cart.objects.get_or_create(user=user)
          print(cart)
          cart_items = CartItem.objects.filter(user=user)
          
          if cart_items:
             if (request.session.get('total')):
                sum = request.session.get('total')
             else:
             # prod = cart_items.get_subtotal()
                sum = cart.get_total_price()
             total = cart.get_total_products()
             coupon = Coupon.objects.all()
             context = {
                 'cart_items': cart_items,
                 'cart': cart,
                 'sum': sum,
                 'total': total,
                 'coupon': coupon,
                 
                 # 'prod': prod,
             }  
             return render(request, 'cart/cart.html', context)
          else:
             message = "Your Cart is Empty"
             return render(request, 'cart/cart.html', {'message': message})
        else:
            raise Exception("User not authenticated")  # Raise an exception if the user is not authenticated
    except Exception as e:
        # Handle the exception appropriately
        # For example, you can log the error or display a user-friendly message
        error_message = f"Error occurred: {str(e)}"
        print(error_message)
        # return redirect('home')
    return render(request,'cart/cart.html', {'error_message': error_message})

def update_cart_items(request):
        print('entered')
        cart = Cart.objects.get(user=request.user)
        cart_item_id = request.GET.get('cart_item_id')
        action = request.GET.get('action')

        # cart_item = Cartitem.objects.get(id=cart_item_id)
        try:
           print('try')
           cart_item = CartItem.objects.get(id=cart_item_id) 
           print(cart_item)
        except cart_item.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Cart item not found'})

        if action == 'increase':
            print("increases")
            if cart_item.product_variant.stock > cart_item.quantity:
                cart_item.quantity += 1
                print(cart_item.quantity)
        elif action == 'decrease':
            cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
        cart_item.save()
        if 'total' in request.session:
            del request.session['total']

        return JsonResponse({'status': 200, 'quantity': cart_item.quantity,'total':cart.get_total_price(),'total_items':cart.get_total_products()})




class Checkout(View):
    
    def get(self, request):
    
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(user=request.user)
            address = BillingAddress.objects.filter(user=request.user)

            if cart_items.exists():
                if (request.session.get('total')):
                    sum = request.session.get('total')
                else:
                    sum = cart.get_total_price()
                total = cart.get_total_products()

                context = {
                    'cart_items': cart_items,
                    'address': address,
                    'sum': sum,
                    'total': total,
                }
                return render(request, 'cart/checkout.html', context)
            else:
                return redirect('cart')  # Redirect to cart page if there are no cart items
        except Cart.DoesNotExist:
            return redirect('cart')  # Redirect to cart page if the user doesn't have a cart

    
class Add_address(CreateView):
    model = BillingAddress
    form_class = BillingAddressForm
    template_name = 'cart/add-address.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('Checkout')


class Add_address_user(CreateView):
    model = BillingAddress
    form_class = BillingAddressForm
    template_name = 'cart/add-address.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_profile')


# edit address checkout page
def edit_address(request, id):
    product = get_object_or_404(BillingAddress, pk=id)
    if request.method == "POST":
        product_form = BillingAddressForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('Checkout')
    else:
        product_form = BillingAddressForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'cart/edit-address.html', context)


# user profile edit address
def edit_address_user(request, id):
    product = get_object_or_404(BillingAddress, pk=id)
    if request.method == "POST":
        product_form =BillingAddressForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('user_profile')
    else:
        product_form = BillingAddressForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'cart/edit-address.html', context)


def delete_address(request, id):
    prod = BillingAddress.objects.get(pk=id)
    prod.delete()
    return redirect('Checkout')


def delete_address_user(request, id):
    prod = BillingAddress.objects.get(pk=id)
    prod.delete()
    return redirect('user_profile')

@login_required(login_url='signin')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'cart/wishlist.html',context)


def add_to_wishlist(request, id):
    myproduct = get_object_or_404(Product, pk=id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=myproduct)
    response_data = {'created': created}
    return JsonResponse(response_data)


def remove_from_wishlist(request, id):
    myproduct = get_object_or_404(Product, pk=id)
    Wishlist.objects.filter(user=request.user, product=myproduct).delete()
    messages.success(request, 'Product removed from wishlist.')
    return redirect('wishlist')







    # cart = Cart.objects.get(user=request.user)
        # cart_items = CartItem.objects.filter(user=request.user)
        # address = Address.objects.filter(user=request.user)
        # if not cart_items.exists():
        #     return redirect('Checkout')
        # sum = cart.get_total_price()
        # total = cart.get_total_products()

        # context = {
        #     'cart_items': cart_items,
        #     'address': address,
        #     'sum': sum,
        #     'total': total,
        # }
        # return render(request, 'checkout.html', context)

        # def update_cart_items(request):
#         cart_item_id = request.GET.get('cart_item_id')
#         action = request.GET.get('action')

#         # cart_item = Cartitem.objects.get(id=cart_item_id)
#         try:
#            print("gdfghfd")
#            cart_item = CartItem.objects.get(id=cart_item_id) 
#         except cart_item.DoesNotExist:
#             return JsonResponse({'status': 404, 'error': 'Cart item not found'})

#         if action == 'increase':
#             print("button pressed")
#             if isinstance(cart_item.product_variant, ProductVariant):
#                 if cart_item.quantity < cart_item.product_variant.stock:
#                     cart_item.quantity += 1
#                     print("increment")
                    

#             # elif isinstance(cart_item.product, Product):
#             #     if cart_item.quantity < cart_item.product.stock:
#             #         cart_item.quantity += 1
                    
            
#         elif action == 'decrease':
#             cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
#         cart_item.save()
#         if 'total' in request.session:
#             del request.session['total'] 
       

#         return JsonResponse({'status': 200,'quantity': cart_item.quantity,'subtotal':cart_item.get_subtotal})
 

# def admin_cart(request):
#     cart = Cart.objects.all()
#     cartitems = Cart.objects.all()
#     return render(request,'cart/admin-cart.html',{'cart':cart,'cartitems':cartitems})