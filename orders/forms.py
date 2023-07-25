from django import forms
from .models import *

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code', 'is_expired', 'discount_price', 'minimum_amount']
        widgets = {
            'coupon_code': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            # 'is_expired': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'is_expired': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'minimum_amount': forms.DateInput(attrs={'class': 'form-control datepicker mb-3'}),
}