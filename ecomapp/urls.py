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
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),

    path("signup/", CustomerSignupView.as_view(), name="customersignup"),
    path("signin/", CustomerSigninView.as_view(), name='customersignin'),
    path("signout/", CustomerSignoutView.as_view(), name="customersignout"),

    path("customer-profile/", CustomerProfileView.as_view(), name="customerprofile"),


    #     admin panel urls
    path("ecom-admin/login/", AdminLoginView.as_view(), name="adminlogin"),
    path("ecom-admin/logout/", AdminLogoutView.as_view(), name="adminlogout"),
    path("ecom-admin/", AdminHomeView.as_view(), name="adminhome"),
    path("ecom-admin/order-<o_id>/",
         AdminOrderDetailView.as_view(), name="adminorderdetail"),
    path("ecom-admin/order-<o_id>/action-<act>/",
         AdminOrderActionView.as_view(), name="adminorderaction"),


]
