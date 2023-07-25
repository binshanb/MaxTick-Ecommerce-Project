from django.urls import path
from . import views
from . views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('place_order',PlaceOrder.as_view(),name="place_order"),
    path('place_order_razorpay',views.place_order_razorpay,name="place_order_razorpay"),
    path('payments_complete/',views.payments_complete,name="payments_complete"),
    # path('place_order/<int:id>/',views.place_order,name="place_order"),
    path('payments/<int:id>/',views.payments,name="payments"),
    path('payment_with_wallet', views.payment_with_wallet,name="payment_with_wallet"),


    path('coupon_manage', views.coupon_manage,name="coupon_manage"),
    path('add_coupons', views.add_coupons,name="add_coupons"),
    path('delete_coupons/<int:id>/', views.delete_coupons,name="delete_coupons"),
    path('edit_coupons/<int:id>/', views.edit_coupons,name="edit_coupons"),
    path('apply_coupon',views.apply_coupon,name="apply_coupon"),

    path('edit_order/<int:id>/', views.edit_order,name="edit_order"),
    path('order_products/<int:id>/', views.order_products,name="order_products"),

    path('cancel_order/<int:id>/', views.cancel_order,name="cancel_order"),
    path('my_orders', views.my_orders,name="my_orders"),
    path('myorder_products/<int:id>/', views.myorder_products,name="myorder_products"),
    path('return_order/<int:id>/', views.return_order,name="return_order"),
    path('wallet', views.wallet,name="wallet"),
    



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


