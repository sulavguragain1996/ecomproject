from django.contrib import admin
from .models import *


admin.site.register([Customer, Product, Category, Admin,
                     ProductImage, CartProduct, Order, Slider, Cart])
