from django.urls import path
from .views import *


app_name = 'ecomapp'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("product/<slug>/detail/",
         ProductDetailView.as_view(), name="productdetail"),
    path("category/<slug>/products/",
         CategoryDetailView.as_view(), name="categorydetail"),

    path("search/", ProductSearchView.as_view(), name="productsearch"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("add-to-cart/<sl>/", AddToCartView.as_view(), name="addtocart"),
    path("manage-cart/<cp_id>-<act>/",
         ManageCartView.as_view(), name="managecart"),

]
