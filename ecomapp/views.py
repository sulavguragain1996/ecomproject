from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, FormView
from django.db.models import Q
from django.urls import reverse
from .models import *
from .forms import *


class HomeView (View):
    def get(self, request):

        context = {
            'allcategory': Category.objects.all(),
            "allsliders": Slider.objects.all()
        }
        cart_id = request.session.get("cid")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            context["mycart"] = cart
        return render(request, 'clienttemplates/home.html', context)


class ProductDetailView(View):

    def get(self, request, slug):
        n = Product.objects.get(slug=slug)
        n.view_count += 1
        n.save()
        context = {
            'productdetail': n,
            'allcategory': Category.objects.all(),
        }
        cart_id = request.session.get("cid")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            context["mycart"] = cart
        return render(request, 'clienttemplates/productdetail.html', context)


class CategoryDetailView(View):
    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        categoryproducts = Product.objects.filter(category=category)
        context = {
            'category': category,
            'categoryproducts': categoryproducts,
            'allcategory': Category.objects.all(),

        }
        cart_id = request.session.get("cid")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            context["mycart"] = cart

        return render(request, 'clienttemplates/categorydetail.html', context)


class ProductSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        context = {
            "searchedproducts": Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(category__title__icontains=query)),
            # same code pass in all to see category in dropdown in all page
            'allcategory': Category.objects.all(),
        }
        cart_id = request.session.get("cid")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            context["mycart"] = cart
        return render(request, "clienttemplates/productsearch.html", context)


class MyCartView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'allcategory': Category.objects.all(),
        }
        cart_id = request.session.get("cid")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            context["mycart"] = cart
        else:
            print("no cart")

        return render(request, "clienttemplates/mycart.html", context)


class AddToCartView(View):
    def get(self, request, sl, *args, **kwargs):
        # sl = self.kwargs['s']
        product = Product.objects.get(slug=sl)
        cart_id = request.session.get("cid")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            try:
                cp = cart.cartproduct_set.get(
                    product=product)  # cartproduct ???
                cp.quantity += 1
                cp.subtotal += product.selling_price
                cp.save()
                cart.total += product.selling_price
                cart.save()
            except Exception as e:
                print(e)
                cp = CartProduct.objects.create(
                    cart=cart, product=product, rate=product.selling_price, quantity=1, subtotal=product.selling_price)
                cart.total += product.selling_price
                cart.save()
        else:
            cart = Cart.objects.create(total=0)
            request.session["cid"] = cart.id
            CartProduct.objects.create(
                cart=cart, product=product, rate=product.selling_price, quantity=1, subtotal=product.selling_price)
            cart.total += product.selling_price
            cart.save()
        # steps
        # check whether user has cart already or not in session
        # if exits, get and use that cart else make a new cart and store its id to session
        # check whether the product is already in the cart.
        context = {
            'allcategory': Category.objects.all(),
            "product": product,
            "mycart": cart
        }
        return render(request, "clienttemplates/addtocart.html", context)


class ManageCartView(View):
    def get(self, request, cp_id, act, * args, **kwargs):
        cp = CartProduct.objects.get(id=cp_id)  # cartproduct (use).. @ cp_id
        cart = cp.cart
        if act == "pls":
            cp.quantity += 1
            cp.subtotal += cp.rate
            cp.save()
            cart.total += cp.rate
            cart.save()
        elif act == "min":
            cp.quantity -= 1
            cp.subtotal -= cp.rate
            cp.save()
            cart.total -= cp.rate
            cart.save()
            if cp.quantity <= 0:
                cp.delete()
        elif act == "rmv":
            cart.total -= cp.subtotal
            cart.save()
            cp.delete()
        else:
            print("Invalid action in cart")
        # return redirect("/my-cart/")
        return redirect("ecomapp:mycart")


class EmptyCartView(View):
    def get(self, request):
        c_id = request.session.get("cid")
        if c_id:
            c = Cart.objects.get(id=c_id)
            c.cartproduct_set.all().delete()
            c.total = 0
            c.save()
        return redirect("ecomapp:mycart")


class CheckoutView(View):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cid")
        try:
            cart = Cart.objects.get(id=cart_id)
            print("cart exists")
        except:
            print("cart doesnot exist")
            return redirect("ecomapp:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("in get method")
        cart_id = request.session.get("cid")
        cart = Cart.objects.get(id=cart_id)

        context = {
            'allcategory': Category.objects.all(),
            "mycart": cart,
            "checkoutform": CheckoutForm  # this is send from forms.py
        }
        return render(request, "clienttemplates/checkout.html", context)

    def post(self, request, *args, **kwargs):
        print("in post method")
        cart_id = request.session.get("cid")
        cart = Cart.objects.get(id=cart_id)
        ordered_by = request.POST.get("ordered_by")
        shipping_address = request.POST.get("shipping_address")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        payment_method = request.POST.get("payment_method")
        Order.objects.create(
            cart=cart, ordered_by=ordered_by, shipping_address=shipping_address, mobile=mobile, email=email,
            subtotal=cart.total, discount=0, total=cart.total, order_status="Order Received", payment_method=payment_method)
        del request.session["cid"]

        return redirect("ecomapp:home")


# class CustomerSignupView(FormView):
#     template_name = "clienttemplates/customersignup.html"
#     form_class = SignupForm
#     success_url = "/"
#     # def get(self, request, *args, **kwargs):
#     #     context = {
#     #         "signupform": SignupForm
#     #     }
#     #     return render(request, "clienttemplates/customersignup.html", context)

#     def form_valid(self, form):
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         full_name = form.cleaned_data.get("full_name")
#         address = form.cleaned_data.get("address")
#         # to create user, use User.objects.create_user(username, email, password)
#         user = User.objects.create_user(email, email, password)
#         customer = Customer.objects.create(
#             user=user, full_name=full_name, address=address)
#         login(self.request, user)
#         return super().form_valid(form)


class CustomerSignupView(FormView):
    def get(self, request, *args, **kwargs):
        context = {
            "signupform": SignupForm
        }
        return render(request, "clienttemplates/customersignup.html", context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        # to create user, use User.objects.create_user(username, email, password)
        if password != confirm_password:
            context = {
                "signupform": SignupForm,
                "err": "Passwords didnot match. "
            }
            return render(request, "clienttemplates/customersignup.html", context)
        try:
            user = User.objects.create_user(email, email, password)
            customer = Customer.objects.create(
                user=user, full_name=full_name, address=address)
            login(self.request, user)
        except:
            context = {
                "signupform": SignupForm,
                "err": "Email already used. "
            }
            return render(request, "clienttemplates/customersignup.html", context)
        return redirect("ecomapp:home")


class CustomerSignoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:home")


# admin views

class AdminLoginView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "adminloginform": AdminLoginForm
        }
        return render(request, "admintemplates/adminlogin.html", context)

    def post(self, request, *args, **kwargs):
        uname = request.POST.get("username")
        pword = request.POST.get("password")
        usr = authenticate(username=uname, password=pword)
        if usr is not None:
            try:
                usr.admin
                login(request, usr)
            except:
                return redirect(reverse("ecomapp:adminlogin") + "?st=err")

        else:
            print(reverse("ecomapp:adminlogin"), "8888888888888888888888888")

            return redirect(reverse("ecomapp:adminlogin") + "?st=err")
        return redirect("ecomapp:adminhome")


class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:adminlogin")


class AdminHomeView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # if Admin.objects.filter(user=request.user).exists():
            #     pass
            # else:
            #     return redirect("ecomapp:adminlogin")
            try:
                request.user.admin
                # Admin.objects.get(user=request.user)
            except:
                return redirect(reverse("ecomapp:adminlogin") + "?st=ua")
        else:
            return redirect(reverse("ecomapp:adminlogin") + "?st=ua")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "neworders": Order.objects.filter(order_status="Order Received").order_by("-id")
        }
        return render(request, "admintemplates/adminhome.html", context)


class AdminOrderDetailView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                request.user.admin
            except:
                return redirect(reverse("ecomapp:adminlogin") + "?st=ua")
        else:
            return redirect(reverse("ecomapp:adminlogin") + "?st=ua")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, o_id, *args, **kwargs):
        context = {
            "order": Order.objects.get(id=o_id)
        }
        return render(request, "admintemplates/adminorderdetail.html", context)
