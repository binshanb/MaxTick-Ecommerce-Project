from django.contrib import admin
from .models import Category,Product,ProductImage,ProductVariant,Color,Brand

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name','slug','description')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','slug','description','price','images','is_available','brand','category')

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'images')

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'color', 'stock', 'price')

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name','price')

class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)





admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImage,ProductImageAdmin)
admin.site.register(ProductVariant,ProductVariantAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Brand,BrandAdmin)

