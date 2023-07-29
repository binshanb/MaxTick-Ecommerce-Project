from django.shortcuts import render,redirect
from django.contrib import messages,auth
import calendar
from django.db.models import Count
from django.db.models.functions import ExtractMonth,ExtractYear,ExtractDay
from django.shortcuts import get_object_or_404
# from multiupload.fields import MultiFileField
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from  django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from store.forms import CategoryForm,ProductImageForm,ProductForm,BrandForm,ColorForm,ProductVariantForm
from django.forms import BaseModelFormSet

from accounts.models import CustomUser
from .forms import DateFilterForm

from store.models import Category,Product,ProductImage,Brand,Color,ProductVariant
from orders.models import Orders,ProductOrder
from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.db.models import Q
from datetime import datetime

# Create your views here.

# add multiple images
ImageFormSet = ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=5)

@never_cache

@login_required(login_url="ad_login")
def ad_home(request):
    delivered_orders = Orders.objects.filter(status='Delivered')
    delivered_orders_by_months = delivered_orders.annotate(delivered_month=ExtractMonth('created_at')).values('delivered_month').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_count')
    print( delivered_orders_by_months)
    delivered_orders_month = []
    delivered_orders_number = []
    for d in delivered_orders_by_months:
         delivered_orders_month.append(calendar.month_name[d['delivered_month']])
         delivered_orders_number.append(list(d.values())[1])


    order_by_months = Orders.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month','count')
    monthNumber = []
    totalOrders = []
    for o in order_by_months:
         monthNumber.append(calendar.month_name[o['month']])
         totalOrders.append(list(o.values())[1])
    # print(delivered_orders_number)

    delivered_orders_by_years = delivered_orders.annotate(delivered_year=ExtractYear('created_at')).values('delivered_year').annotate(delivered_count=Count('id')).values('delivered_year', 'delivered_count')
    delivered_orders_year = []
    delivered_orders_year_number = []
    for d in delivered_orders_by_years:
        delivered_orders_year.append(d['delivered_year'])
        delivered_orders_year_number.append(d['delivered_count'])
    
    order_by_years = Orders.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year', 'count')
    yearNumber = []
    totalOrdersYear = []
    for o in order_by_years:
        yearNumber.append(o['year'])
        totalOrdersYear.append(o['count'])
    
    context ={
         'delivered_orders':delivered_orders,
         'order_by_months':order_by_months,
         'monthNumber':monthNumber,
         'totalOrders':totalOrders,
         'delivered_orders_number':delivered_orders_number,
         'delivered_orders_month':delivered_orders_month,
         'delivered_orders_by_months':delivered_orders_by_months,
         'order_by_years': order_by_years,
         'yearNumber': yearNumber,
         'totalOrdersYear': totalOrdersYear,
         'delivered_orders_year': delivered_orders_year,
         'delivered_orders_year_number': delivered_orders_year_number,
         'delivered_orders_by_years': delivered_orders_by_years,


    }

    return render(request,"admin/ad-home.html",context)

def sales_report(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'admin/sales-report.html', context)


# views.py



def sales_date(request):
    if request.method == 'GET':
        form = DateFilterForm(request.GET)
        # order_by_date = Orders.objects.annotate(month=ExtractDay('created_at')).values('day').annotate(count=Count('id')).values('day','count')
        # totalOrders = []
        # for o in order_by_date:
        #  totalOrders.append(list(o.values())[1])

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Query the sales data within the specified date range
            
            sales_data = Orders.objects.filter(created_at__range=[start_date, end_date].order_by("-created_at"))

            return render(request, 'admin/sales-report-daily.html', {'sales_data': sales_data, 'form': form,})

    else:
        form = DateFilterForm()

    return render(request, 'admin/sales-report-daily.html', {'form': form})



def sales_report_by_products(request,id):
    product = Product.objects.get(pk=id)
    orders = ProductOrder.objects.filter(product=product)
    s = product.variant.all()
    total_stock = 0
    for s in s:
      total_stock += s.stock
      
    delivered_orders = []
    delivered_quantity = 0
    for order in orders:
        if order.order.status == 'Delivered':
           delivered_orders.append(order)
           delivered_quantity += order.quantity
    
    number_delivered_orders = len(delivered_orders)

    
    context = {
        'product':product,
        'orders':orders,
        'delivered_quantity':delivered_quantity,
        'number_delivered_orders':number_delivered_orders,
        'total_stock':total_stock,
    }
    

    return render(request, 'admin/sales-report-productwise.html',context)

@never_cache

def ad_login(request):
    if request.user.is_authenticated:
        return redirect('ad_home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['Password']
        user = authenticate(email=email,password=password)

        if user.is_superuser:
            login(request,user)
            return redirect("ad_home")
        else:
            messages.error(request,"User name or password is incorect")
            return redirect('ad_login')
    return render(request,"admin/ad-login.html")

# admin logout
def ad_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request,"Logged out Successfully")
    return redirect('ad_login')


def ad_search(request):
    users = []
    if request.method == 'POST':
        query = request.POST['query']
        users = CustomUser.objects.filter(Q(email__icontains=query))
    return render(request, "admin/ad-search.html",{'users':users})

@login_required(login_url="ad_login")
def user_info(request):
    stud = CustomUser.objects.all()
    return render(request, "admin/user-info.html", {'stud':stud})



def block_user(request, email):
    if request.method == "POST":
        user = CustomUser.objects.get(email=email)
        user.is_active = False
        user.save()
        return redirect('user_info')
    
    
def unblock_user(request, email):
    if request.method == "POST":
        user = CustomUser.objects.get(email=email)
        user.is_active = True
        user.save()
        return redirect('user_info')
    
@login_required(login_url="ad_login")    
def category_info(request):
    cat = Category.objects.all()
    context = {
        'cat' : cat,
    }
    return render(request,"admin/category-info.html",context)


@login_required(login_url="ad_login")
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_info')
    else:
        form = CategoryForm()
    context = {
        "form": form
    }
    return render(request,'admin/add-category.html', context)
    
# This Function will Delete
def edit_category(request, id):
    category = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        category_form = CategoryForm(request.POST,instance=category)
        if category_form.is_valid():
            category_form.save()
            return redirect('category_info')
    else:
        category_form = CategoryForm(instance=category)

    context = {
        "category_form": category_form
    }
    return render(request,'admin/edit-category.html', context)

def delete_category(request, id):
    if request.method == 'POST':
        pi = Category.objects.get(pk=id)
        pi.delete()
        return redirect('category_info')

@login_required(login_url="ad_login")
def product_info(request):
    pro = Product.objects.all()
    context = {
        'pro' : pro,
    }
    return render(request,"admin/product-info.html",context)

ImageFormSet = ProductImageFormSet = inlineformset_factory(Product,ProductImage,form=ProductImageForm,extra=5)  
@never_cache   
@login_required(login_url='ad_login') 

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    image_form = ProductImageFormSet(request.POST, request.FILES, instance=Product())

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        image_form = ProductImageFormSet(request.POST, request.FILES, instance=Product())

        if product_form.is_valid() and image_form.is_valid():
            product_form.save()
            image_form.save()
            return redirect('product_info')
    else:
        product_form = ProductForm(instance=product)
        image_form = ProductImageFormSet(instance=product)

    context = {
        'product_form': product_form,
        'image_form': image_form,
    }

    return render(request, 'admin/edit-product.html', context)


# def edit_product(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == "POST":
#         product_form = ProductForm(request.POST, request.FILES, instance=product)
#         image_form = ProductImageFormSet(request.POST, request.FILES, instance=Product())
#         if product_form.is_valid() and image_form.is_valid():
#             myproduct = product_form.save(commit=False)
#             myproduct.save()
#             return redirect('product_info')
#     else:
#         product_form = ProductForm(instance=product)
#         image_form = ProductImageFormSet(instance=Product())

#     context = {
#         "product_form": product_form,
#         'image_form' : image_form,
#     }
#     return render(request, 'admin/edit-product.html', context)


def delete_product(request, id):
    if request.method == "POST":
        prod = Product.objects.get(pk=id)
        prod.delete()
        return redirect('product_info')
ImageFormSet = ProductImageFormSet = inlineformset_factory(Product,ProductImage,form=ProductImageForm,extra=5)    
@never_cache   
@login_required(login_url='ad_login')
def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST,request.FILES)
        image_form = ProductImageFormSet(request.POST, request.FILES, instance=Product())
        if product_form.is_valid() and image_form.is_valid():
            myproduct = product_form.save(commit=False)
            myproduct.save()
            image_form.instance = myproduct
            image_form.save()
            
            return redirect("product_info")
    else:
        product_form = ProductForm()
        image_form = ProductImageFormSet(instance=Product())
    
    context = {
        'product_form': product_form,
        'image_form' : image_form,
                }

    return render(request,"admin/add-product.html",context)


@login_required(login_url="ad_login")

def variant(request):
    pro = ProductVariant.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin/variant.html', context)

def delete_variant(request, id):
    if request.method == "POST":
        prod = ProductVariant.objects.get(pk=id)
        prod.delete()
        return redirect('variant')
    
def add_variant(request):
    if request.method == "POST":
        variant_form = ProductVariantForm(request.POST,request.FILES)
        # image_form = ProductImageFormSet(request.POST, request.FILES, instance=product())
        if variant_form.is_valid():
            # myproduct = product_form.save(commit=False)
            variant_form.save()
            # image_form.instance = myproduct
            # image_form.save()
            # return redirect('products')
            return redirect("variant")
    else:
        variant_form = ProductVariantForm()
        # image_form = ProductImageFormSet(instance=product())
    context = {'variant_form': variant_form}
    return render(request, 'admin/add-variant.html', context)

def edit_variant(request, id):
    product = get_object_or_404(ProductVariant, pk=id)
    if request.method == "POST":
        variant_form = ProductVariantForm(request.POST, request.FILES, instance=product)
        if variant_form.is_valid():
            variant_form.save()
            return redirect('variant')
    else:
        variant_form = ProductVariantForm(instance=product)

    context = {
        "variant_form": variant_form
    }
    return render(request, 'admin/edit-variant.html', context)



@login_required(login_url="ad_login")

def brand(request):
    pro = Brand.objects.all()
    context = {
      'pro': pro
    }
    return render(request,"admin/brand-info.html",context)

def del_brand(request,id):
    if request.method == "POST":
        prod = Brand.objects.get(pk=id)
        prod.delete()
        return redirect('brand')
    
def edit_brand(request,id):
    brand = get_object_or_404(Brand,pk=id)
    if request.method == "POST":
        brand_form = BrandForm(request.POST,instance=brand)
        if brand_form.is_valid():
            brand_form.save()
            return redirect('brand')
    else:
        brand_form = BrandForm(instance=brand)
    context = {
        'brand_form':brand_form
    }
    return render(request,"admin/edit-brand.html",context)

def add_brand(request):
    if request.method == "POST":
        brand_form = BrandForm(request.POST,request.FILES)
        # image_form = ProductImageFormSet(request.POST, request.FILES, instance=product())
        if brand_form.is_valid():
            # myproduct = product_form.save(commit=False)
            brand_form.save()
            # image_form.instance = myproduct
            # image_form.save()
            # return redirect('products')
            return redirect("brand")
    else:
        brand_form = BrandForm()
        # image_form = ProductImageFormSet(instance=product())
    context = {'brand_form': brand_form}
    return render(request,'admin/add-brand.html',context)


@login_required(login_url="ad_login")
        
def color(request):
    prod = Color.objects.all()
    context = {
      'prod': prod
    }
    return render(request,"admin/color-info.html",context)

def del_color(request,id):
    if request.method == "POST":
        prod = Color.objects.get(pk=id)
        prod.delete()
        return redirect('color')
    
def edit_color(request,id):
    product = get_object_or_404(Color,pk=id)
    if request.method == "POST":
        color_form = ColorForm(request.POST,request.FILES,instance=product)
        if color_form.is_valid():
            color_form.save()
            return redirect('color')
    else:
        color_form = ColorForm(instance=product)
    context = {
        'color_form':color_form
    }
    return render(request,"admin/edit-color.html",context)

def add_color(request):
    if request.method == "POST":
        color_form = ColorForm(request.POST,request.FILES)
        if color_form.is_valid():
            color_form.save()
            return redirect("color")
    else:
        color_form = ColorForm()
    context = {'color_form': color_form}
    return render(request, 'admin/add-color.html', context)




# def ad_myorder(request):
#     order = Orders.objects.all()
#     return render(request, 'admin/ad-myorder.html', {'order':order})


def ad_myorders(request):

    order = Orders.objects.all().order_by("-created_at")

    return render(request, 'admin/ad-myorder.html', {'order':order})

def ad_order_search(request):
    users = []
    if request.method == 'POST':
        query = request.POST['query']
        # orders = CustomUser.objects.filter(Q(email_icontains=query)|Q(id_contains=query))
        orders = Orders.objects.filter(Q(user__email__icontains=query)).order_by("-created_at")

        # order = Order.objects.filter(order=orders)
    return render(request, "admin/ad-order-search.html", {'orders':orders})
