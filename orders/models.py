from django.db import models
from accounts.models import *
from store.models import *
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Payments(models.Model):
    payment_choices=(
        ('COD','COD'),
        ('Razorpay','Razorpay'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100,choices=payment_choices)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.name}--{self.payment_method}"
    

class Orders(models.Model):
    STATUS = (
        ('New','New'),
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('out for shipping','out for shipping'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')
       )

    user    = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payments, on_delete=models.SET_NULL, blank=True, null= True) 
    address = models.ForeignKey(BillingAddress, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=50)
    order_note = models.CharField(max_length=50, blank=True)
    order_total = models.FloatField()
    return_reason =models.TextField(blank=True)
    tax = models.FloatField(null=True)
    status = models.CharField(max_length=50,choices=STATUS,default='New')
    ip = models.CharField(max_length=50,blank=True)
    is_ordered = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.order_number is not None:
            return self.order_number
        else:
            return "No order number available"
    
    # def full_address(self):
    #     return f'{self.address_line_1} {self.address_line_2}'
    
    
class ProductOrder(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="myorders")
    payment = models.ForeignKey(Payments, on_delete=models.SET_NULL,blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariant,on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    product_price = models.FloatField(null=True)
    ordered = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    
    def str(self):
        return f"{self.product} - {self.quantity}"
    

class Coupon(models.Model): 
    coupon_code = models.CharField(max_length = 10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default = 100)
    minimum_amount = models.IntegerField(default=500)
    
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   

    def str(self):
        return f"Wallet for {self.user.username}"







# class Coupon(models.Model):
#     coupon_code = models.CharField(max_length=10)
#     is_expired = models.BooleanField(default=False)
#     discount_price = models.IntegerField(default=100)
#     minimum_amount = models.IntegerField(default=500)
#     usage_count = models.PositiveIntegerField(default=0)
