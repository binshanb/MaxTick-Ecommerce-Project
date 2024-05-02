from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
# from django.core.files.base import File
# from django.db.models.base import Model
# from django.forms.utils import ErrorList
from . models import CustomUser,BillingAddress
import re
from django.core.exceptions import ValidationError


class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'last_name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    phone_number = PhoneNumberField(region="IN",max_length=15, required=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','phone_number','password1','password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Regular expression to match the desired phone number format
        phone_number_pattern = re.compile(r'^\+\d{1,3}\d{6,14}$')  # Modify this pattern as per your desired format
        
        if not phone_number_pattern.match(phone_number):
            raise ValidationError("Please enter a valid phone number in the format: +XXXXXXXXXXXX")
        
        return phone_number

    def clean(self):
        cleaned_data = super(CustomUserForm, self).clean()
        password1 = cleaned_data.get('password1') 
        password2 = cleaned_data.get('password2')  

        if password1 != password2:
            raise forms.ValidationError("Password and confirm password don't match!")
        
class VerifyForm(forms.Form):
    code = forms.CharField(
        max_length=8,
        required=True,
        help_text='Enter code',
        widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Enter code here'})
    )


class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ["name","house_name", "address_line_1", "city", "state", "country", "phone", "pincode"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'house_name': forms.Textarea(attrs={'class': 'form-control mb-3'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'city': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'state': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'country': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control mb-3'}),
            
        }