from django.contrib import messages,auth
from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from .models import CustomUser,BillingAddress
from . import verify
from django.contrib.auth.tokens import default_token_generator
from store.models import Product,Category
from cart.models import Cart
from  orders.models import Orders
from . forms import CustomUserForm,VerifyForm,BillingAddressForm
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
# Create your views here.


def home(request):
    #  products = Product.objects.all().filter(is_available=True)
    #  context = {
    
    #     'products':products,
    #      }
     return render(request,"home.html")
@never_cache
def signup(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            # phone_number =(form.cleaned_data.get('phone_number')) 
            form.save()
            
            return redirect('signin')
    else:
        form = CustomUserForm()
    return render(request, 'accounts/register.html',{'form':form})

@never_cache
def signin(request):

    if request.user.is_authenticated:
        return redirect('home')

    email = request.session.get('email')
    if email:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass1']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            request.session['email']=email
            messages.success(request, 'Logged in Successfully')

            return render(request,'home.html')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('signin')

    return render(request,'accounts/login.html')

@never_cache
def signout(request):
    logout(request)
    request.session.flush()
    messages.error(request,"Logged out successfuly")
    return redirect('home')

def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            phone_number=request.session.get('phone')
            

            if verify.check(phone_number, code):
                user = CustomUser.objects.get(email=request.session.get('username'))
                user.is_active = True
                user.is_verified = True
                user.save()
                if user is not None:
                    login(request,user)
                    return redirect('home')
             
                return redirect('home')
    else:
        form = VerifyForm()
    return render(request,'accounts/otpverify.html',{'form': form})

def phone_verify(request):
    if request.method == "POST":
        phone = '+91'+  str(request.POST['phone_number'])
        print(phone)
        if check_phone_number(phone):
            verify.send(phone)
            user = checkuser(phone)
            request.session['username'] = user.email

            user.is_verified = True
            user.is_active = True
            request.session['phone'] = phone
            return redirect(verify_code)
        else:
            context = "Please register first"
            return render(request,'accounts/otpphone.html',{'context':context})
    return render(request,'accounts/otpphone.html')


def checkuser(phone):
    user = CustomUser.objects.filter(phone_number=phone).first()
    return user

def check_phone_number(phone_number):
    try:
        phone_number = CustomUser.objects.filter(phone_number=phone_number).first()
        print(phone_number)
        return True
    except CustomUser.DoesNotExist:
        return False
    
def about(request):
   return render(request,"accounts/about.html")

def contact(request):
   return render(request,"accounts/contact.html")

# user profile function
@login_required(login_url='signin')
def user_profile(request):
    address = BillingAddress.objects.filter(user=request.user)
    # order = Orders.objects.get(user=request.user)
    try:
        order = Orders.objects.filter(user=request.user)
    except Orders.DoesNotExist:
        order = None


    context = {
        'address': address,
        'order': order,
    }
    return render(request, 'accounts/user-profile.html', context)

def edit_profile(request):
    address = BillingAddress.objects.filter(user=request.user)

    # order = Orders.objects.get(user=request.user)
    try:
        order = Orders.objects.filter(user=request.user)
    except Orders.DoesNotExist:
        order = None


    context = {
        'address': address,
        'order': order,
   
    }
    return render(request, 'accounts/edit-profile.html', context)

def forgot_password(request):
    global mobile_number_forgotPassword
    if request.method == 'POST':
        # setting this mobile number as global variable so i can access it in another view (to verify)
        mobile_number_forgotPassword = request.POST.get('phone_number')
        # checking the null case
        if mobile_number_forgotPassword is '':
            messages.warning(request, 'You must enter a mobile number')
            return redirect('forgot_password')
   
        # instead we can also do this by savig this mobile number to session and
        # access it in verify otp:
        # request.session['mobile']= mobile_number
        user = CustomUser.objects.filter(phone_number=mobile_number_forgotPassword)
        if user:  #if user exists
            verify.send('+91' + str(mobile_number_forgotPassword))
            return redirect('forgot_password_otp')
        else:
            messages.warning(request,'Mobile number doesnt exist')
            return redirect('forgot_password')
            
    return render(request, 'accounts/forgotpassword.html')


def forgot_password_otp(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('code')
        # otp = request.POST.get('otp')
        if verify.check('+91'+ str(mobile_number), otp):
            user = CustomUser.objects.get(phone_number=mobile_number)
            if user:
                return redirect('reset_password')
        else:
            messages.warning(request,'Invalid OTP')
            return redirect('enter_otp')
    else:
        form = VerifyForm()
        
    return render(request,'accounts/forgot-password-otp.html', {'form':form})


def reset_password(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        print(str(password1)+' '+str(password2)) #checking
        
        if password1 == password2:
            user = CustomUser.objects.get(phone_number=mobile_number)
            print(user)
            print('old password  : ' +str(user.password))
            
            user.set_password(password1)
            user.save()

            print('new password  : ' +str(user.password))
            messages.success(request, 'Password changed successfully')
            return redirect('signin')
        else:
            messages.warning(request, 'Passwords doesnot match, Please try again')
            return redirect('reset_password')
    
    return render(request, 'accounts/resetpassword.html')
       
    


    # product = get_object_or_404(BillingAddress, pk=id)
    # if request.method == "POST":
    #     product_form =BillingAddressForm(request.POST, request.FILES, instance=product)
    #     if product_form.is_valid():
    #         product_form.save()
    #         return redirect('user_profile')
    # else:
    #     product_form = BillingAddressForm(instance=product)

    # context = {
    #     "product_form": product_form
    # }
    # return render(request, 'accounts/edit-profile.html',context)
    


