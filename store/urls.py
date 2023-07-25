from django.urls import path
from . import views

urlpatterns= [

    path('store/',views.store,name="store"),
    path('store/<slug:category_slug>/', views.store, name="products_by_category"),
    path('search', views.search,name="search"),
    path('product_detail/<int:id>/', views.product_detail,name="product_detail"),
    path('filter-data',views.filter_data,name='filter_data'),
    # path('filter_price', views.filter_price, name='filter_price'),
    # path('filter_brands', views.filter_brands, name='filter_brands'),


    

    # path('search_brand', views.search_brand,name="search_brand"),
    # path('store/<slug:category_slug>/', views.store, name="products_by_category"),
    # path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name="product_detail"),
    
    
    

]