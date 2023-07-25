from django.urls import path
from . import views

urlpatterns= [
    path('',views.home,name="home"),
    path('signin',views.signin,name="signin"),
    path('signup',views.signup,name="signup"),
    path('signout',views.signout,name="signout"),
    path('ver', views.verify_code,name="ver"),
    path('phone_verify', views.phone_verify,name="phone_verify"),

    path('forgot_password', views.forgot_password,name="forgot_password"),
    path('forgot_password_otp', views.forgot_password_otp,name="forgot_password_otp"),
    path('reset_password', views.reset_password,name="reset_password"),


    path('about', views.about,name="about"),
    path('contact', views.contact,name="contact"),
    path('user_profile', views.user_profile,name="user_profile"),
    path('edit_profile', views.edit_profile,name="edit_profile"),

]