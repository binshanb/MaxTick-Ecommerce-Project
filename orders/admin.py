from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Payments)
admin.site.register(Orders)
admin.site.register(ProductOrder)
admin.site.register(Coupon)
admin.site.register(Wallet)


