from django import forms
from .models import *


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address',
                  "mobile", "email", "payment_method"]
        widgets = {
            "ordered_by": forms.TextInput(attrs={
                "class": 'form-control',
                "placeholder": "Enter your name..."
            }),
            "shipping_address": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "mobile": forms.NumberInput(attrs={
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),
            "payment_method": forms.Select(attrs={
                "class": "form-control"
            })
        }
