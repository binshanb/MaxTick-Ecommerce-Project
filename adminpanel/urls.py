from django.urls import path
from . import views

urlpatterns= [

    path('ad_home/',views.ad_home,name="ad_home"),
    path('ad_login',views.ad_login,name="ad_login"),
    path('ad_logout',views.ad_logout,name="ad_logout"),

    path('sales_report',views.sales_report,name="sales_report"),
    path('sales_report_by_products/<int:id>/',views.sales_report_by_products,name="sales_report_by_products"),

    path('user_info',views.user_info,name="user_info"),
    path('ad_search', views.ad_search,name="ad_search"),
    path('block_user/<str:email>', views.block_user, name='block_user'),
    path('unblock_user/<str:email>', views.unblock_user,name="unblock_user"),

    path('category_info',views.category_info,name="category_info"),
    path('edit_category/<int:id>/',views.edit_category,name="edit_category"),
    path('add_category',views.add_category,name="add_category"),
    path('delete_category/<int:id>',views.delete_category,name="delete_category"),

    path('product_info',views.product_info,name="product_info"),
    path('edit_product/<int:id>/', views.edit_product,name="edit_product"),
    path('delete_product/<int:id>/', views.delete_product,name="delete_product"),
    path('add_product', views.add_product,name="add_product"),

    path('brand', views.brand,name="brand"),
    path('edit_brand/<int:id>/', views.edit_brand,name="edit_brand"),
    path('del_brand/<int:id>/', views.del_brand,name="del_brand"),
    path('add_brand', views.add_brand,name="add_brand"),

    path('color', views.color,name="color"),
    path('edit_color/<int:id>/', views.edit_color,name="edit_color"),
    path('del_color/<int:id>/', views.del_color,name="del_color"),
    path('add_color', views.add_color,name="add_color"),

    path('variant', views.variant,name="variant"),
    path('delete_variant/<int:id>/', views.delete_variant,name="delete_variant"),
    path('edit_variant/<int:id>/', views.edit_variant,name="edit_variant"),
    path('add_variant', views.add_variant,name="add_variant"),

    path('ad_myorders', views.ad_myorders,name="ad_myorders"),

    

    
    


  



 

]