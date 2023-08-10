from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from cart.models import CartItem
from django.db.models import Q
from django.contrib import messages
from django.db.models import Min, Max
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse


# Create your views here.

   



def store(request, category_slug=None):

    if request.method=="POST":
        selected_min_price = request.POST['min_price']
        selected_max_price = request.POST['max_price']
        selected_category = request.POST['selected_category']
        print(selected_min_price)
        print(selected_max_price)
        print(selected_category)

        complex_lookup = Q(price__gte=selected_min_price) & Q(price__lte=selected_max_price)
        # filter_data= Product.objects.filter(category__category_name = selected_category,(Q(price__gte=min_price) & Q(price__lte=max_price)))
        filter_data = Product.objects.filter(complex_lookup,category__category_name=selected_category)
       
       
       
        
        print(filter_data)
        return render(request,'store/store.html',{'products':filter_data})


    

    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)
    min_price = products.aggregate(Min('price'))['price__min']
    max_price = products.aggregate(Max('price'))['price__max']
    
    selected_min_price = request.GET.get('selectedMinPrice',min_price)
    selected_max_price = request.GET.get('selectedMaxPrice',max_price)
    selected_category = request.GET.get('category_selected')
    print("firstone",selected_category)


	
    if category_slug != None:
        selected_category = get_object_or_404(Category, slug=category_slug)
        
        # categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=selected_category)
        print("products",products)
        # products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    if selected_min_price and selected_max_price:
        products = products.filter(price__gte=selected_min_price, price__lte=selected_max_price)
        print("3",selected_category)
        if selected_category:
            c = Category.objects.get(category_name=selected_category)
      
            products = products.filter(category=c.id)
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
        for p in paged_products:
             print(p.product_name)

     
    context = {
        'products': paged_products,
        'product_count': product_count,
        'min_price': min_price,
        'max_price' : max_price,
        # 'selected_category': selected_category,
        # 'selected_min_price': selected_min_price,
        # 'selected_max_price': selected_max_price,
        'categories': categories,
       
      
    }
    return render(request,'store/store.html',context)





def product_detail(request,id):
    pro = Product.objects.get(pk=id)
    print(pro)
    var = ProductVariant.objects.filter(product_name=pro)
    print(var)
    context ={
        'pro':pro,
        'var':var,
    }
    return render(request, 'store/product-detail.html',context)

def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('brand').filter(Q(description__icontains=keyword) |Q(product_name__icontains=keyword)) 
            
 

    product_count = products.count()
    
    context = {
        'products': products,
        'product_count':product_count,

    }

    return render(request,'store/search.html',context)


# Filter Data
# def filter_data(request):
#     print("hello")
#     if request.method=="POST":
#         selected_category=request.POST.get('selected_category')   

#     return render(request,'store/store.html')
    
	# categories=request.GET.getlist('categories[]')


	
	# minPrice=request.GET['minPrice']
	# maxPrice=request.GET['maxPrice']
	# allProducts=Product.objects.all().order_by('-id').distinct()
	# allProducts=allProducts.filter(product__price__gte=minPrice,product__price__lte=maxPrice)

        
   
	# if len(categories)>0:
	# 	allProducts=allProducts.filter(category__id__in=categories).distinct()
	

	# t =render_to_string('store/store.html',{'data':allProducts})
	# return JsonResponse({'data':t})

# def filter_price(request):
#     print("entered")
#     product = Product.objects.all()
#     price_filter_form = PriceFilterForm(request.GET or None)
#     if price_filter_form.is_valid():
#         min_price = price_filter_form.cleaned_data['min_price']
#         max_price = price_filter_form.cleaned_data['max_price']
#         product = [product for product in product if any(variant.price >= min_price and variant.price <= max_price for variant in product.variant.all())]

#     context ={
#         'product':product
#     }
#     return render(request,'store/filter-price.html',context)

# def filter_brands(request):
#     print("entered")
#     brand_id = request.GET.get('brand', None)
#     products = Product.objects.all()
#     if brand_id:
#         products=products.filter(brand_id=brand_id)

# # Pass the filtered products to the template
#     context = {
#        'products': products,
#        'brand_filter_form': BrandFilterForm(request.GET or None)
#        }
#     return render(request, 'store/filter-brands.html', context)






   

    



    
    
    
    
    
    
    
    
    
    # def brand(request):
#     product = Product.objects.filter(gender="Brand")
#     return render(request, "store/brand.html", {'product':product})


# def price(request):
#     product = Product.objects.filter(gender="Price")
#     return render(request, "store/price.html", {'product':product})

# def search_brand(request):
#      product = []
#      if request.method == 'POST':
#         query = request.POST['query']
#         product = Product.objects.filter(Q(id__contains=query)|Q(Brand__brand_name__icontains=query))
#      return render(request, "store/search-brand.html", {'product':product}) 
    
    
    
    
    
    
    
    # try:
    #     single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    # except Exception as e:
    #     rpro = Product.objects.get(pk=id)
    # var = ProductVariant.objects.all()aise e
    
    # context = {
    #     'single_product':single_product
    # }
    
    # return render(request, 'store/product-detail.html',context)
    # 
    # size = Size.objects.all()
    # color = Color.objects.all()
    
    
  
    #     in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    # except Exception as e:
    #     raise e

    # if request.user.is_authenticated:
    #     try:
    #         orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    #     except OrderProduct.DoesNotExist:
    #         orderproduct = None
    # else:
    #     orderproduct = None

    # # Get the reviews
    # # reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # # Get the product gallery
    # # product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    # context = {
    #     'single_product': single_product,
    #     'in_cart'       : in_cart,
    #     'orderproduct': orderproduct,
    #     'reviews': reviews,
    #     'product_gallery': product_gallery,
    # }
    # return render(request, 'store/product_detail.html', context)


