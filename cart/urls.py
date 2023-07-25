from django.urls import path
from . import views
from . views import *
# from  orders.views import payments
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('cart/',views.cart,name="cart"),
    path('add_to_cart', views.add_to_cart,name="add_to_cart"),
    path('delete_cart_item/<int:id>/', views.delete_cart_item,name="delete_cart_item"),
    path('update_cart_items', views.update_cart_items,name="update_cart_items"),
    

    path('checkout', Checkout.as_view(),name="Checkout"),
    path('add_address', Add_address.as_view(),name="Add_address"),
    path('add_address_user', Add_address_user.as_view(),name="Add_address_user"),

    path('edit_address/<int:id>/', views.edit_address,name="edit_address"),
    path('edit_address_user/<int:id>/', views.edit_address_user,name="edit_address_user"),

    path('delete_address/<int:id>/', views.delete_address,name="delete_address"),
    path('delete_address_user/<int:id>/', views.delete_address_user,name="delete_address_user"),

    path('wishlist', views.wishlist,name="wishlist"),
    path('add_to_wishlist/<int:id>/', views.add_to_wishlist,name="add_to_wishlist"),
    path('remove_from_wishlist/<int:id>/', views.remove_from_wishlist,name="remove_from_wishlist"),

    

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)