from django.db import models
from accounts.models import *
from store.models import *

# Create your models here.




class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # def __str__(self):
    #     return self.user.first_name

    # def get_total_price(self):
    #     return sum(item.get_subtotal() for item in self.cart_items.all())

    def get_total_price(self):
        if self.cart_items.exists():
            return sum(item.get_subtotal() for item in self.cart_items.all())
        else:
            return 0
    
    def get_total_products(self):
        return sum(item.quantity for item in self.cart_items.all())


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_item_product')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.product.product_name} - ProductVariant:{self.product_variant.color}"

    def get_subtotal(self):
        return self.product_variant.price * self.quantity
    

class GuestUser(models.Model):
    uid = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.uid
    

User = get_user_model()
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
