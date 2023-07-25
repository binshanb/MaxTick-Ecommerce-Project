from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe
from accounts.models import CustomUser

# Create your models here.

class Category(models.Model):

    category_name = models.CharField(max_length=50,unique=True)
    slug = AutoSlugField(populate_from='category_name',unique=True,null=True,default=None)
    description = models.CharField(max_length=255,blank=True)
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])
    
    def __str__(self):
        return self.category_name
    
class Brand(models.Model):

    brand_name = models.CharField(max_length=200,unique=True)
    slug = AutoSlugField(populate_from='brand_name',unique=True,null=True,default=None)

    def __str__(self):
        return self.brand_name
    
class Product(models.Model):

    product_name = models.CharField(max_length=200,unique=True)
    slug = AutoSlugField(populate_from='product_name',unique=True,null=True,default=None)
    description  = models.TextField(max_length=500,blank=True)
    price        = models.IntegerField(default=0)
    # stock        = models.IntegerField(default=0)
    images        = models.ImageField(upload_to='images/products/')
    is_available  =models.BooleanField(default=True)
    category  =models.ForeignKey(Category,on_delete=models.CASCADE)
    brand     =models.ForeignKey(Brand,on_delete=models.CASCADE)

    # def get_url(self):
    #     return reverse('product_detail',args=[self.category.slug,self.slug])

    def __str__(self):
        return self.product_name
    
class Color(models.Model):

    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    def __str__(self)->str:
        return self.name
    
class ProductVariant(models.Model):
    
    product_name=models.ForeignKey(Product, on_delete=models.CASCADE,related_name="variant")
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.IntegerField(default=0)

    @property
    def quantity(self):
        return self.stock

    def __str__(self):
        return f"{self.product_name} - {self.color}"

    # class Meta:
    #     unique_together = ('product_name', 'size', 'color')

    


    # def __str__(self) -> str:
    #     return f"{self.product_name.product_name} - Color:{self.color.name}"
    
    
class ProductImage(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    images = models.ImageField(upload_to='images/products', blank=True)

    def _str_(self):
        return self.images.url
    
class Watch(models.Model):
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.brand


