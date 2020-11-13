from django import forms
from .models import *
from django.contrib.auth.models import User


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


class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Enter you username..."
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Enter you password..."
    }))


class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
    }))
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
    }))

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if User.objects.filter(username=email).exists():
    #         raise forms.ValidationError(
    #             "Customer with this email already exists. ")
    #     return email
