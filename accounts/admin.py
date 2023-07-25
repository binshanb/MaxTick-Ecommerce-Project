from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,BillingAddress

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'last_login', 'date_joined', 'is_active')



admin.site.register(CustomUser)
admin.site.register(BillingAddress)