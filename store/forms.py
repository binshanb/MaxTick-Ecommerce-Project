from django import forms
from .models import Product,Category,ProductImage,Brand,Color,ProductVariant
from decimal import Decimal

class CategoryForm(forms.ModelForm):
    class Meta:
       model =  Category
       fields = ["category_name","description"]

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']

class ProductForm(forms.ModelForm):
    price = forms.CharField(widget=forms.NumberInput),
    images = forms.ImageField(label='Product Image', required=True, error_messages={'required': 'Please upload an image.'})
    class Meta:
        model = Product
        fields = ["product_name","description", "price", "is_available", "category","images","brand"]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'brand': forms.Select(attrs={'class': 'form-control mb-3'}),
            # 'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'category': forms.Select(attrs={'class': 'form-control mb-3'}),
            
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product_name','images']


class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['name','price']

class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product_name','color','stock','price']
        # widgets = {
        #     'product_name': forms.Select(attrs={'class': 'form-control mb-3'}),
        #     'color': forms.Select(attrs={'class': 'form-control mb-3'}),
        #     'stock': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
        #     'price': forms.DecimalField(max_digits=8, decimal_places=2),
            
        # }

class PriceFilterForm(forms.Form):
    min_price = forms.DecimalField(decimal_places=2)
    max_price = forms.DecimalField(decimal_places=2)


class BrandFilterForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), empty_label="All Brands", required=False)
