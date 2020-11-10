from django.contrib import admin
from .models import *


admin.site.register([Customer, Product, Category,
                     ProductImage, CartProduct, Order, Slider, Cart])
