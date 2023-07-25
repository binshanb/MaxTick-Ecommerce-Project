from typing import Any
from django.views import View
from django.shortcuts import render, redirect
from .models import *

from accounts.models import *
from django.shortcuts import get_object_or_404
from store.models import *
from cart.models import *
# from .models import *
from django.http import JsonResponse
from .forms import *
from cart.views import *
from datetime import date
import datetime
from django.views.decorators.http import require_POST
import json
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
import uuid
import decimal
import razorpay
# Create your views here.




class PlaceOrder(View):

        def dispatch(self, request, *args, **kwargs):
                # Declare and assign instance attributes
                
                self.flag = 0
                print("place")
                self.current_user = request.user
                print(self.current_user)

                self.cart = Cart.objects.get(user=self.current_user)
                self.cart_items = CartItem.objects.filter(user=self.current_user)
                self.cart_count = self.cart_items.count()
                
                self.total_price = self.cart.get_total_price()
                print(self.cart_count)
                self.default_address_id = None
                # Call the default dispatch method
                return super().dispatch(request, *args, **kwargs)
                        
                
            
        def get(self,request):
            
            
          # if cart count is less than or equal to zero redirect back to homepage
            if self.cart_count <= 0:
                    return redirect('home')
            else:
                print("else")
                try:
                        current_order = Orders.objects.get(user=self.current_user)
                        print(current_order,"current")
                        if current_order:
                                data = self.current_order
                        else:
                                raise Exception("order not formed")
                except Exception as e:
                        print("exception")
                        data = Orders()
                        print(data)

                        
                        data.user = self.current_user
                        selected_option = request.GET.get('selectedOption')
                        payment_method_mapping = {
                                        'cod': 'COD',
                                        'razorpay': 'Razorpay',
                                        # Add more mappings as needed
                                }
                        print(selected_option)
                        payment_method_selected = payment_method_mapping.get(selected_option)
                        # status =''
                        # if payment_method_selected == 'COD':
                        #         status = 'Pending'
                        # else:
                        #         status = 'Success'

                        print(payment_method_selected)
                        if selected_option == 'cod':
                                print("first one")
                                payment_method = Payments.objects.create(user=self.current_user,payment_method=payment_method_selected,amount_paid=self.total_price,status="Pending")
                                
                                data.payment = payment_method
                                
                                self.default_address_id = request.GET.get('defaultAddressId')
                                print(self.default_address_id)
                                data.address =  BillingAddress.objects.get(id=self.default_address_id)
                                
                                data.order_total = self.total_price
                                
                                data.save()
                                print(data)
                                # generate order number
                              
                              
                               
                                timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
                                unique_id = str(uuid.uuid4().int)[:6]
                                order_number = f"{timestamp}{unique_id}"
                               
                                order_number=order_number
                                data.order_number = order_number
                                print(data.order_number)
                                data.save()
                                for item in self.cart_items:
                                        order = ProductOrder.objects.create(product=item.product,
                                                variation=item.product_variant,
                                                payment=payment_method,
                                                order=data,
                                                quantity=item.quantity,
                                                product_price=item.product_variant.price,
                                                user=self.current_user,
                                                ordered=True)
                                        print(order)
                               
                                        pv = item.product_variant
                                        pv.stock -= item.quantity
                                        print(pv.stock)
                                        pv.save()
                                        if 'total' in request.session:
                                                del request.session['total']
                                        item.delete()
                                        flag = 1
                                
                                # return JsonResponse({'message': 'Order placed successfully.','flag':flag})
                                redirect_url = reverse('payments_complete') + f'?amount={self.total_price}&order_number={order_number}&payment_id={payment_method.id}'
                                return JsonResponse({'message': 'Order placed successfully.','flag':flag,'id':order_number,'amount':self.total_price,'redirect':redirect_url})
                        elif selected_option == 'razorpay':
                                    print("elif")
                                    import razorpay
                                    client = razorpay.Client(auth=("rzp_test_KrqLewTjkr6SCu", "TGZYNRQpe8MX0kohW9VQ6Ebg"))
                
                                    razorpay_order = client.order.create(
                                    {"amount": int(self.total_price), "currency": "INR", "payment_capture": "1"}
                                    )
                                    print(razorpay_order)
                                    
                                    order_id = razorpay_order['id']
                                    
                                    print(order_id)
                                        

                                    payment_method = Payments.objects.create(user=self.current_user,payment_method=payment_method_selected,amount_paid=self.total_price,status="Success")
                                        
                                    data.payment = payment_method
                                        
                                    default_address_id = request.GET.get('defaultAddressId')
                                    data.address =  BillingAddress.objects.get(id=default_address_id)
                                    print(data.address)
                                    data.order_total = self.total_price
                                    print(data.user,data.payment,data.address,data.order_total)
                                    data.save()
                                    print(data)
                                    # generate order number
                                        
                                    timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
                                    unique_id = str(uuid.uuid4().int)[:6]
                                    order_number = f"{timestamp}{unique_id}"
                            
                                    data.order_number =order_number
                                    print(data.order_number)
                                    data.save()
                                    for item in self.cart_items:
                                        order = ProductOrder.objects.create(product=item.product,
                                                variation=item.product_variant,
                                                payment=payment_method,
                                                order=data,
                                                
                                                quantity=item.quantity,
                                                product_price=item.product_variant.price,
                                                user=self.current_user,
                                               
                                                ordered=True)
                                        print(order)
                                        # if 'total' in request.session:
                                        #         del request.session['total']
                                        item.delete()
                                        pv = item.product_variant
                                        pv.stock -= item.quantity
                                        print(pv.stock)
                                        pv.save()
                                    
                                #     cart = Cart.objects.get(user=request.user)
                                #     total_price = cart.get_total_price()
                                    payment_id = payment_method.id
                                    redirect_url = reverse('place_order_razorpay') + f'?total={self.total_price}&id={order_id}&order_number={order_number}&payment_id={payment_id}'
                                    return JsonResponse({'message': 'razorpay entered.','redirect':redirect_url})

def place_order_razorpay(request):
        # total = request.GET.get('total')
        if (request.session.get('total')):
                total = request.session.get('total')
                razor= total
        else:
                total = request.GET.get('total')
                razor=total
        try:
                total = float(total) * 100
        except (TypeError, ValueError):
                total = 0
        # total = total * 100
        if 'total' in request.session:
                del request.session['total']
        print(total)
        id = request.GET.get('id')
        print(id)
        order_number = request.GET.get('order_number')
        context = {
                'total': total,
                'id': id,
                'order_number':order_number,
                'razor':razor
        }
        return render(request, "orders/razorpay.html", context)


def payments_complete(request):
        id = request.GET.get('id')
        payment_id = request.GET.get('razorpay_payment_id')
        amount = request.GET.get('amount')
        print(amount)
        order_number = request.GET.get('order_number')
        
        context = {
                'id': id,
                'payment_id': payment_id,
                'amount': amount,
                'order_number':order_number

        }

        return render(request, "orders/payments-complete.html",context)


def order_products(request, id):
    orders = Orders.objects.get(pk=id)
    myorder = ProductOrder.objects.filter(order=orders)
    context = {
        'orders': orders,
        'myorder':myorder
    }
    return render(request, 'admin/ad-productorders.html',context)



def payments(request,id):
    # cart = get_object_or_404(Cart, user=request.user)
    cart = Cart.objects.get(user=request.user)
    cart_items=CartItem.objects.filter(cart=cart)
    adds = BillingAddress.objects.get(pk=id)
    if (request.session.get('total')):
        sum = request.session.get('total')
    else:
        sum = cart.get_total_price()
    total = cart.get_total_products()
    wallet = Wallet.objects.get(user=request.user)
    
    if wallet.balance >= sum:
        flag = 1
    else:
        flag = 0
    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    print(sum)
      
   
    payment = client.order.create({ "amount": sum*100, "currency": "INR", "receipt": "order_rcptid_11" })


    context = {
            'sum': sum,
            'total': total,
            'adds': adds,
            'payment':payment,
            'cart_items':cart_items,
            'flag':flag
        }
    return render(request, 'orders/payments-cod.html', context)  


def payment_with_wallet(request):
          
        current_user = request.user
        wallet = Wallet.objects.get(user=current_user)
        cart = Cart.objects.get(user=current_user)
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        total_price = cart.get_total_price()
        
                
            
          # if cart count is less than or equal to zero redirect back to homepage
        if cart_count <= 0:
                return redirect('home')
        else:        
               
                data = Orders()

                data.user = current_user

                payment_method = Payments.objects.create(user=current_user,payment_method='Wallet',amount_paid=total_price,status=False)
                
                data.payment = payment_method
                
                default_address_id = request.GET.get('defaultAddressId')
                print(default_address_id)
                data.address =  BillingAddress.objects.get(id=default_address_id)
                print(data.address)
                data.order_total = total_price
                print(data.user,data.payment,data.address,data.order_total)
                data.save()
                print(data)
                                
                timestamp = timezone.now().strftime('%Y%m%d%H%M%S%f')
                unique_id = str(uuid.uuid4().int)[:6]
                order_number = f"{timestamp}{unique_id}"
                data.order_number = order_number
                
                data.save()
                for item in cart_items:
                        order = ProductOrder.objects.create(user=request.user,
                                product=item.product,
                                variation=item.product_variant,
                                payment=payment_method,
                                order=data,
                                quantity=item.quantity,
                                product_price=item.product_variant.price,
                                ordered=True)
                        print(order)
                        print(item.product_variant.stock)
                        p = item.product_variant
                        p.stock -= item.quantity
                        print(item.product_variant.stock)
                        p.save()
                        item.delete()
                        
                cart.coupon = None
                cart.save()
                wallet.balance = float(wallet.balance) - float(total_price)
                wallet.save()
                redirect_url = reverse('payments_complete') + f'?amount={total_price}&order_number={order_number}&payment_id={payment_method.id}'
                return JsonResponse({'message': 'Order placed successfully.','id':order_number,'amount':total_price,'redirect':redirect_url})


def my_orders(request):

    order = ProductOrder.objects.filter(user=request.user).order_by("-created_at")
    orders = Orders.objects.filter(user=request.user).order_by("-created_at")

    
    context = {
        'order':order,
        'orders':orders,
        
    }

    return render(request, 'orders/my-orders1.html',context)

def myorder_products(request, id):
    orders = Orders.objects.get(pk=id)
    myorder = ProductOrder.objects.filter(order=orders)
    context = {
        'orders': orders,
        'myorder':myorder,
    }
    return render(request, 'orders/my-orders-prodetails.html', context)

def edit_order(request, id):
    if request.method == "POST":
        status = request.POST.get("status")
        try:
            order = Orders.objects.get(pk=id)
            order.status = status
            order.save()
        except Orders.DoesNotExist:
            pass
    return redirect("ad_myorders")




def cancel_order(request,id):
    print(id)
    if request.method == "POST":
        cancellation_reason = request.POST.get('cancellation_reason')
        try:
        
            order = get_object_or_404(Orders, pk=id, user=request.user)
            orders=ProductOrder.objects.filter(order=order)
            order.status = 'Cancelled'
            order.cancellation_reason = cancellation_reason
            order.save()
            
            if order.status == 'Cancelled':
                for product in orders:
                    product.variation.stock += product.quantity
                    product.variation.save()
                 
            if order.payment.payment_method =='Razorpay'or 'COD':
                wallet, _ =Wallet.objects.get_or_create(user=request.user)
                refund_amount=decimal.Decimal(order.order_total)
                wallet.balance += refund_amount
                wallet.save()

        except Orders.DoesNotExist:
            pass

    return redirect("my_orders")


#order return function
def return_order(request,id):
    print(id)
    if request.method=="POST":
        return_reason=request.POST.get('return_reason')
        try:
            order = get_object_or_404(Orders, pk=id, user= request.user)
            order.status='Return'
            order.return_reason = return_reason
            order.save()
            if order.payment.payment_method == 'Razorpay' or 'COD':
                wallet, _ = Wallet.objects.get_or_create(user=request.user)
                refund_amount = decimal.Decimal(order.order_total)
                print(refund_amount)
                wallet.balance += refund_amount
                wallet.save()

        except Orders.DoesNotExist:
            pass
    return redirect('my_orders')



def coupon_manage(request):
    coupons = Coupon.objects.all()
    context = {
        "coupons" : coupons
    }
    return render(request,'orders/coupon.html', context)

def add_coupons(request):
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            coupon_form.save()
            return redirect('coupon_manage')
    else:
        coupon_form = CouponForm()

    context = {'coupon_form': coupon_form}
    return render(request, 'orders/add-coupons.html', context)

def delete_coupons(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        coup.delete()
    return redirect('coupon_manage')

def edit_coupons(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        coupon_form = CouponForm(request.POST, instance=coup)
        if coupon_form.is_valid:
            coupon_form.save()
        return redirect('coupon_manage')
    else:
        coup = Coupon.objects.get(id=id)
        coupon_form = CouponForm(instance=coup)
        context = {
            "coupon_form" : coupon_form
        }
    return render(request, 'orders/edit-coupons.html',context)   

def apply_coupon(request):
    print('Coupon starts')
    if request.method == 'POST':
        data = {}
        body = json.loads(request.body)
        coupon_code = body.get('coupon')
        print(coupon_code)
        total_price = body.get('grand_total')
        print(total_price)

        try:
            coupon = Coupon.objects.get(coupon_code__iexact=coupon_code, is_expired=False)
        except Coupon.DoesNotExist:
            data['message'] = 'Not a Valid Coupon'
            data['total'] = total_price
        else:
            if coupon.is_expired:
                data['message'] = 'Coupon Already Used'
                data['total'] = total_price
            else:
                min_amount = coupon.minimum_amount
                discount_price = coupon.discount_price
                print(discount_price)
                if total_price >= min_amount:
                    total_price -= discount_price
                    request.session['total'] = total_price
                    coupon.is_expired = True
                    coupon.save()
                    print(total_price)
                    data['message'] = f'{coupon.coupon_code} Applied'
                    data['total']= total_price
                    print(data)
                else:
                    data['message'] = 'Not a Valid Coupon'
                    data['total'] = total_price
                    print(data)

        return JsonResponse(data)

def wallet(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
        if wallet:
            print(wallet.balance)
    except:
        wallet = Wallet.objects.create(user=request.user, balance=0)
    return render(request,'orders/wallet.html',{'wallet':wallet})












# @require_POST
# def apply_coupon(request):
#     body = json.loads(request.body)
#     grand_total = int(body['grand_total'])
#     print(grand_total)
#     coupon_code = body['coupon']
#     print(coupon_code)
#     try:
#         coupon = Coupon.objects.get(coupon_code=coupon_code)
#         print(coupon)
#     except Coupon.DoesNotExist:
#         data = {
#             "total": grand_total,
#             "message": "Not a Valid Coupon"
#         }
#     else:
        

#         min_amount = int(coupon.minimum_amount)
#         if min_amount < grand_total :
#             grand_total = grand_total - int(coupon.discount_price)
#             request.session['total'] = grand_total  # Update the session variable
#             data = {
#                 "total": grand_total,
#                 "message": f"{coupon.coupon_code} Applied"
#             }
#         else:
#             data = {
#                 "total": grand_total,
#                 "message": "Not a Valid Coupon"
#             }
#     return JsonResponse(data)
                        













# def apply_coupon(request):
#     body = json.loads(request.body)
#     grand_total = int(body['grand_total'])
#     coupon_code = body['coupon']
    
#     try:
#         coupon = Coupon.objects.get(coupon_code=coupon_code)

#         if coupon.is_expired:
#             data = {
#                 "total": grand_total,
#                 "message": "Coupon has expired and is no longer valid."
#             }
#         elif coupon.usage_count > 0:
#             data = {
#                 "total": grand_total,
#                 "message": "Coupon has already been used and is no longer valid."
#             }
#         else:
#             min_amount = int(coupon.minimum_amount)
#             if min_amount < grand_total:
#                 grand_total = grand_total - int(coupon.discount_price)
#                 request.session['total'] = grand_total  # Update the session variable
#                 coupon.usage_count += 1  # Increment the usage count
#                 if coupon.usage_count == 1:
#                     coupon.is_expired = True  # Mark coupon as expired after first use
#                 coupon.save()
#                 data = {
#                     "total": grand_total,
#                     "message": f"{coupon.coupon_code} Applied"
#                 }
#             else:
#                 data = {
#                     "total": grand_total,
#                     "message": "Not a Valid Coupon"
#                 }
#     except Coupon.DoesNotExist:
#         data = {
#             "total": grand_total,
#             "message": "Not a Valid Coupon"
#         }

#     return JsonResponse(data)



# def cancel_order(request,order_id):  

#     # Retrieve the order object
#     order = get_object_or_404(Orders, id=order_id, user=request.user)
#     print(order.status)

#     if order.status != 'Pending':
#         # Check if the order can be canceled (e.g., if it's still pending)
#         messages.error(request, 'This order cannot be canceled.')
#         return redirect(reverse('my_orders'))

#     # Cancel the order
#     order.status = 'CANCELLED'
#     order.save()

#     # Add a success message
#     messages.success(request, 'Order has been canceled successfully.')

#     return redirect(reverse('my_orders'))

# def return_order(request,id):
#     print(id)
#     if request.method=="POST":
#         return_reason=request.POST.get('return_reason')
#         try:
#             order=get_object_or_404(Orders, pk=id, user= request.user)
#             order.status='Return'
#             order.save()
#             timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
#             unique_id = str(uuid.uuid4().fields[-1])[:8]
#             tracking_number=f'{timestamp}-{unique_id}'
#             order_return=Orders.objects.create(order=order,return_reason=return_reason,tracking_number=tracking_number)
#             order_return.save()
#         except Orders.DoesNotExist:
#             pass
#     return redirect('my_orders')










# def orders_complete(request):
#         id = request.GET.get('id')
#         payment_id = request.GET.get('razorpay_payment_id')
#         amount = request.GET.get('amount')
#         print(amount)
#         adds = request.user.BillingAddress.adds
#         context = {

#                 'id': id,
#                 'payment_id': payment_id,
#                 'amount': amount,
                
#         }

#         return render(request, "orders/orders-complete.html",context)
# class PlaceOrder(View):

#     def get(self,request,id,payment_method):
    
#         # Retrieve user, address, and other necessary data from the request
#         user = request.user
#         address = BillingAddress.objects.get(id=id)
#         payment_method = payment_method  
#         status=''
#         if payment_method=='Razorpay':
#             status='Success'
#         else:
#             status='Pending'

#         # Retrieve the user's cart or order items
#         cart = Cart.objects.get(user=request.user)
#         # cart = get_object_or_404(Cart, user=request.user)
#         total_price = cart.get_total_price()

#         # Create a new payment entry
#         payment = Payments.objects.create(
#             user=user,
#             payment_method=payment_method,
#             amount_paid=total_price, 
#             status=status  # Set initial status to Pending
#         )

#         # Create a new order
#         order = Orders.objects.create(
#             user=user,
#             payment=payment,
#             address=address,
#             order_number='...',  
#             order_note='...',  
#             order_total=total_price,  
#             tax=0.0,  
#             status='New',  
#             ip='...', 
#             is_ordered=False  
#         )

#         # Create OrderProduct instances for each cart item and update the order total
#         cart_items = CartItem.objects.filter(user=request.user)
#         for cart_item in cart_items:
#             ProductOrder.objects.create(
#                 order=order,
#                 payment=payment,
#                 user=user,
#                 product=cart_item.product,
#                 variation=cart_item.product_variant,
#                 quantity=cart_item.quantity,
#                 product_price=cart_item.product.price,
#                 ordered=False
#             )
          
#             order.save()
#             if isinstance(cart_item.product_variant, ProductVariant):
#                 variant = cart_item.product_variant
#                 variant.stock -= cart_item.quantity
#                 variant.save()
#             elif isinstance(cart_item.product, Product):
#                 product = cart_item.product
#                 product.stock -= cart_item.quantity
#                 product.save()
            

#         # Clear the user's cart or order items
#         # Assuming you have a way to clear the cart items for the user
#         cart_items.delete()
        

#         # Redirect to a success page or show a success message
#         return JsonResponse({'success': True , 'message': 'Order placed successfully.'})
    
# def my_view(request):
#     id = 123
#     payment_method = 'Online'
#     url = reverse('place_order', kwargs={'id': id, 'payment_method': payment_method})



# def calculate_cart_total(cart_items):
#     total_price = 0

#     for cart_items in cart_items:
#         total_price += cart_items.total

#     return total_price
# def payments(request,id):
#     address=BillingAddress.objects.get(id=id)
#     cart = Cart.objects.get(user=request.user)
#     total_price = cart.get_total_price()

#     context={
#         'address':address,
#         'cart': cart,
#         'total':total_price
#     }

#     return render(request, 'orders/payments.html',context)

# class PlaceOrderView(View):

#     def get(self, request, id,payment_method):
#         # Retrieve user, address, and other necessary data from the request
#         user = request.user
#         address = BillingAddress.objects.get(id=id)
#         payment_method = payment_method  
#         status=''
#         if payment_method=='Online':
#             status='Success'
#         else:
#             status='Pending'

#         # Retrieve the user's cart or order items
#         cart_items = CartItem.objects.filter(user=request.user)
#         total_price = cart.get_total_price()

#         # Create a new payment entry
#         payment = Payments.objects.create(
#             user=user,
#             payment_method=payment_method,
#             amount_paid=total_price, 
#             status=status  # Set initial status to Pending
#         )

#         # Create a new order
#         order = Orders.objects.create(
#             user=user,
#             payment=payment,
#             address=address,
#             order_number='...',  
#             order_note='...',  
#             order_total=total_price,  
#             tax=0.0,  
#             status='New',  
#             ip='...', 
#             is_ordered=False  
#         )

#         # Create OrderProduct instances for each cart item and update the order total
#         for cart_item in cart_items:
#             ProductOrder.objects.create(
#                 order=order,
#                 payment=payment,
#                 user=user,
#                 product=cart_item.Product,
#                 variation=cart_item.variant,
#                 quantity=cart_item.quantity,
#                 product_price=cart_item.Product.price,
#                 ordered=False
#             )
          
#             order.save()
#             if isinstance(cart_item.variant, ProductVariant):
#                 variant = cart_item.variant
#                 variant.quantity_in_stock -= cart_item.quantity
#                 variant.save()
#             elif isinstance(cart_item.Product, Product):
#                 product = cart_item.Product
#                 product.quantity_in_stock -= cart_item.quantity
#                 product.save()
            

#         # Clear the user's cart or order items
#         # Assuming you have a way to clear the cart items for the user
#         cart_items.delete()

#         # Redirect to a success page or show a success message
#         return HttpResponse("Order placed successfully!")




# def place_order(request,id):
#        # Retrieve user, address, and other necessary data from the request
#         user = request.user
#         address=BillingAddress.objects.get(id=id)  
#         payment_method = 'COD'  # Set the payment method to COD
#          # Retrieve the user's cart or order items
#         cart = Cart.objects.get(user=request.user)
#         total_price = cart.get_total_price()

#         # Create a new payment entry
#         payment = Payments.objects.create(
#             user=user,
#             payment_method=payment_method,
#             amount_paid=total_price,  # Set initial amount to 0 for COD
#             status='Pending'  # Set initial status to Pending
#         )

#         # Create a new order
#         order = Orders.objects.create(
#             user=user,
#             payment=payment,
#             address=address,
#             order_number='...',  # Set your order number accordingly
#             order_note='...',  # Set your order note if needed
#             order_total=total_price,  # Set initial total to 0.0
#             tax=0.0,  # Set initial tax to 0.0
#             status='New',  # Set initial status to New
#             ip='...',  # Set the IP address accordingly
#             is_ordered=False  # Set initial is_ordered to False
#         )

       
        

#         # Create OrderProduct instances for each cart item and update the order total
#         cart_items= CartItem.objects.filter(user=request.user)
#         for cart_item in cart_items:
#             ProductOrder.objects.create(
#                 order=order,
#                 payment=payment,
#                 user=user,
#                 product=cart_item.product,
#                 variation=cart_item.product_variant,
#                 quantity=cart_item.quantity,
#                 product_price=cart_item.product.price,
#                 ordered=False
#             )
#             # order.order_total += cart_item.Product.price * cart_item.quantity
#             order.save()

#         # Clear the user's cart or order items
#         # Assuming you have a way to clear the cart items for the user
#         cart_items.delete()

#         # Redirect to a success page or show a success message
#         return HttpResponse("Order placed successfully!")   

























# class place_order(View):

#         def dispatch(self, request, *args, **kwargs):
#                 # Declare and assign instance attributes
                
#                 self.flag = 0
#                 print("place")
#                 self.current_user = request.user
#                 print(self.current_user)

#                 self.cart = Cart.objects.get(user=self.current_user)
#                 self.cart_items = CartItem.objects.filter(user=self.current_user)
#                 self.cart_count = self.cart_items.count()
                
#                 self.total_price = self.cart.get_total_price()
#                 print(self.cart_count)
#                 self.default_address_id = None
#                 # Call the default dispatch method
#                 return super().dispatch(request, *args, **kwargs)
                        
                
            
#         def get(self,request):
            
            
#           # if cart count is less than or equal to zero redirect back to homepage
#             if self.cart_count <= 0:
#                     return redirect('home')
#             else:
#                 print("else")
#                 try:
#                         current_order = Orders.objects.get(user=self.current_user)
#                         print(current_order,"current")
#                         if current_order:
#                                 data = self.current_order
#                         else:
#                                 raise Exception("order not formed")
#                 except Exception as e:
#                         print("exception")
#                         data = Orders()
#                         print(data)

                        
#                         data.user = self.current_user
#                         selected_option = request.GET.get('selectedOption')
#                         payment_method_mapping = {
#                                         'cod': 'COD',
#                                         'razorpay': 'Razorpay',
#                                         # Add more mappings as needed
#                                 }
#                         print(selected_option)
#                         payment_method_selected = payment_method_mapping.get(selected_option)
#                         print(payment_method_selected)
#                         if selected_option == 'cod':
#                                 print("first one")
#                                 payment_method = Payments.objects.create(user=self.current_user,payment_method=payment_method_selected,amount_paid=self.total_price,status=False)
                                
#                                 data.payment = payment_method
                                
#                                 self.default_address_id = request.GET.get('defaultAddressId')
#                                 print(self.default_address_id)
#                                 data.shipping_address =  BillingAddress.objects.get(id=self.default_address_id)
#                                 print(data.shipping_address)
#                                 data.order_total = self.total_price
#                                 print(data.user,data.payment,data.shipping_address,data.order_total)
#                                 data.save()
#                                 print(data)
#                                 # generate order number
#                                 yr = int(datetime.date.today().strftime('%Y'))
#                                 dt = int(datetime.date.today().strftime('%d'))
#                                 mt = int(datetime.date.today().strftime('%m'))
#                                 d = datetime.date(yr,mt,dt)
#                                 current_date = d.strftime("%Y%m%d")
#                                 order_number= current_date + str(data.id)
#                                 data.order_number = order_number
#                                 print(data.order_number,current_date)
#                                 data.save()
#                                 for item in self.cart_items:
#                                         order = ProductOrder.objects.create(product=item.product,
#                                                 variation=item.product_variant,
#                                                 payment=payment_method,
#                                                 order=data,
#                                                 quantity=item.quantity,
#                                                 product_price=item.product_variant.price,
#                                                 user=self.current_user,
#                                                 ordered=True)
#                                         print(order)
#                                         print(item.product.stock)
#                                         product = item.product
#                                         product.stock -= item.quantity
#                                         print(item.product.stock)
#                                         product.save()
#                                         item.delete()
#                                         flag = 1
                                
#                                 return JsonResponse({'message': 'Order placed successfully.','flag':flag})
                        
# 








#                         
# 
# 
# 
# 
# 
# 
# 
# elif selected_option == 'razorpay':
#                                     print("elif")

#                                     import razorpay
#                                     client = razorpay.Client(auth=("rzp_test_9PWZXmd88RGOGY", "CMlBW52kdSRZWeoUu5Dlt3Qv"))
                
#                                     razorpay_order = client.order.create(
#                                     {"amount": int(self.total_price), "currency": "INR", "payment_capture": "1"}
#                                     )
#                                     print(razorpay_order)
                                    
#                                     order_id = razorpay_order['id']
                                    
#                                     print(order_id)
                                        

#                                     payment_method = Payments.objects.create(user=self.current_user,payment_method=payment_method_selected,amount_paid=self.total_price,status=False)
                                        
#                                     data.payment = payment_method
                                        
#                                     default_address_id = request.GET.get('defaultAddressId')
#                                     data.shipping_address =  BillingAddress.objects.get(id=default_address_id)
#                                     print(data.shipping_address)
#                                     data.order_total = self.total_price
#                                     print(data.user,data.payment,data.shipping_address,data.order_total)
#                                     data.save()
#                                     print(data)
#                                     # generate order number
#                                     yr = int(datetime.date.today().strftime('%Y'))
#                                     dt = int(datetime.date.today().strftime('%d'))
#                                     mt = int(datetime.date.today().strftime('%m'))
#                                     d = datetime.date(yr,mt,dt)
#                                     current_date = d.strftime("%Y%m%d")
#                                     order_number= current_date + str(data.id)
#                                     data.order_number = order_number
#                                     print(data.order_number,current_date)
#                                     data.save()
#                                     for item in self.cart_items:
#                                         order = ProductOrder.objects.create(product=item.product,
#                                                 variation=item.product_variant,
#                                                 payment=payment_method,
#                                                 order=data,
#                                                 quantity=item.quantity,
#                                                 product_price=item.product_variant.price,
#                                                 user=self.current_user,
#                                                 ordered=True)
#                                         print(order)
#                                         item.delete()
#                                         item.product.stock -= item.quantity
                                    
                                    
#                                     payment_id = payment_method.id
#                                     redirect_url = reverse('razorpay') + f'?total={razorpay_order_total}&id={order_id}&order_number={order_number}&payment_id={payment_id}'
    
#                                     return JsonResponse({'message': 'razorpay entered.','redirect':redirect_url})

# # class razorpay(place_order):
#        def get(self,request):
#               print(self.total_price)
             
#               return render(request,'orders/razorpay.html')



# class place_order(View):

#         def dispatch(self, request, *args, **kwargs):
#                 # Declare and assign instance attributes
                
#                 self.flag = 0
#                 print("place")
#                 self.current_user = request.user
#                 print(self.current_user)

#                 self.cart = Cart.objects.get(user=self.current_user)
#                 self.cart_items = CartItem.objects.filter(user=self.current_user)
#                 self.cart_count = self.cart_items.count()
                
#                 self.total_price = self.cart.get_total_price()
#                 print(self.cart_count)
#                 self.default_address_id = None
#                 # Call the default dispatch method
#                 return super().dispatch(request, *args, **kwargs)
                        
                
            
#         def get(self,request):
            
            
#           # if cart count is less than or equal to zero redirect back to homepage
#             if self.cart_count <= 0:
#                     return redirect('home')
#             else:
#                 print("else")
#                 try:
#                         current_order = Orders.objects.get(user=self.current_user)
#                         print(current_order,"current")
#                         if current_order:
#                                 data = self.current_order
#                         else:
#                                 raise Exception("order not formed")
#                 except Exception as e:
#                         print("exception")
#                         data = Orders()
#                         print(data)

                        
#                         data.user = self.current_user
#                         selected_option = request.GET.get('selectedOption')
#                         payment_method_mapping = {
#                                         'cod': 'COD',
#                                         'razorpay': 'Razorpay',
#                                         # Add more mappings as needed
#                                 }
#                         print(selected_option)
#                         payment_method_selected = payment_method_mapping.get(selected_option)
#                         print(payment_method_selected)
#                         if selected_option == 'cod':
#                                 print("first one")
#                                 payment_method = Payments.objects.create(user=self.current_user,payment_method=payment_method_selected,amount_paid=self.total_price,status=False)
                                
#                                 data.payment = payment_method
                                
#                                 self.default_address_id = request.GET.get('defaultAddressId')
#                                 print(self.default_address_id)
#                                 data.shipping_address =  BillingAddress.objects.get(id=self.default_address_id)
#                                 print(data.shipping_address)
#                                 data.order_total = self.total_price
#                                 print(data.user,data.payment,data.shipping_address,data.order_total)
#                                 data.save()
#                                 print(data)
#                                 # generate order number
#                                 yr = int(datetime.date.today().strftime('%Y'))
#                                 dt = int(datetime.date.today().strftime('%d'))
#                                 mt = int(datetime.date.today().strftime('%m'))
#                                 d = datetime.date(yr,mt,dt)
#                                 current_date = d.strftime("%Y%m%d")
#                                 order_number= current_date + str(data.id)
#                                 data.order_number = order_number
#                                 print(data.order_number,current_date)
#                                 data.save()
#                                 for item in self.cart_items:
#                                         order = ProductOrder.objects.create(product=item.product,
#                                                 variation=item.product_variant,
#                                                 payment=payment_method,
#                                                 order=data,
#                                                 quantity=item.quantity,
#                                                 product_price=item.product_variant.price,
#                                                 user=self.current_user,
#                                                 ordered=True)
#                                         print(order)
#                                         print(item.product.stock)
#                                         product = item.product
#                                         product.stock -= item.quantity
#                                         print(item.product.stock)
#                                         product.save()
#                                         item.delete()
#                                         flag = 1
                                
#                                 return JsonResponse({'message': 'Order placed successfully.','flag':flag})
                        
# def place_order_razorpay(request):
#               current_user = request.user
#               flag = 0
#               cart = Cart.objects.get(user=current_user)
#               cart_items = CartItem.objects.filter(user=current_user)
#               cart_count = cart_items.count()

#               if cart_count <= 0:
#                     return redirect('home')
#               else:
#                     total_price = cart.get_total_price()

#                     if request.method == 'GET':
#                         try:
#                               current_order = Orders.objects.get(user=current_user)
#                               if current_order:
#                                     data = current_order
#                               else:
#                                     raise Exception("Order not formed")
#                         except Exception as e:
#                               print("exception")
#                               data = Orders()

#                         data.user = current_user
#                         selected_option = request.GET.get('selectedOption')
#                         payment_method_mapping = {
#                          'razorpay': 'RAZORPAY',
#                          # Add more mappings as needed
#                         }
#                         print(selected_option)
#                         payment_method_selected = payment_method_mapping.get(selected_option)
#                         print(payment_method_selected)
#                         if selected_option == 'razorpay':
#                             print("fourth one")
#                             payment_method = Payments.objects.create(
#                                   user=current_user,
#                                   payment_method='razorpay',
#                                   amount_paid=str(total_price),  # Convert Decimal to string
#                                   status=False
#                          )

#                         data.payment = payment_method
#                         data.name = request.GET.get('first')
#                         data.address_line_1 = request.GET.get('address_line_1')
#                         data.city = request.GET.get('city')
#                         data.state = request.GET.get('state')
#                         data.Pincode = request.GET.get('Pincode')
#                         data.country = request.GET.get('country')
#                         data.Phone = request.GET.get('Phone')
#                         data.Email = request.GET.get('Email')
#                         data.order_total = total_price
                
#                         print(data.user,data.payment,data.address_1,data.order_total)

#                         data.save()

#                         # Generate order number
#                         current_date = datetime.date.today().strftime('%Y%m%d')
#                         order_number = current_date + str(data.id)
#                         data.order_number = order_number
#                         print(data.order_number,current_date)
#                         data.save()

#                         for item in cart_items:
#                               order_product = ProductOrder.objects.create(
#                                     order=data,
#                                     payment=payment_method,
#                                     ProductVariant=item.product_variant,
#                                     quantity=item.quantity,
#                                     price=item.product_variant.price,
#                                     ordered=True
#                                )
#                               print(order_product)
                
#                               flag = 1
                
#                         #delete cart items after order is placed
#                         cart_items.delete()
#                         cart.delete()

#                     client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
#                     print("key")
#                     payment = client.order.create({
#                       'amount': total_price,  # Convert Decimal to integer in paise/cents
#                       'currency': 'INR',
#                       'payment_capture': 1
#                     })
#                     cart.razor_pay_order_id=payment['id']
#                     cart.save()
#                     print('*****************')
#                     print(payment)
#                     amounts=int(total_price*100)
#                     ids=payment['id']
#                     print('*****************')

#                     cart_data = {
#                        'cart_id': cart.cart_id,
#                         # Add other cart attributes as needed
#                     }

#                     context = {'cart': cart_data, 'payment': payment,'amounts':amounts,'ids':ids}

#                     return JsonResponse({'message': 'Order placed successfully', 'flag':flag, 'context':context})