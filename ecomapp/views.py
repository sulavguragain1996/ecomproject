from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import Q
from .models import *


class HomeView (View):
    def get(self, request):

        context = {
            'allcategory': Category.objects.all(),
            "allsliders": Slider.objects.all()
        }
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

        return render(request, 'clienttemplates/categorydetail.html', context)


class ProductSearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        context = {
            "searchedproducts": Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(category__title__icontains=query)),
            # same code pass in all to see category in dropdown in all page
            'allcategory': Category.objects.all(),
        }
        return render(request, "clienttemplates/productsearch.html", context)


class MyCartView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'allcategory': Category.objects.all(),
        }
        cart_id = request.session.get("cid")
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            context["cart"] = cart
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
                cp = cart.cartproduct_set.get(product=product)
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
            "product": product
        }
        return render(request, "clienttemplates/addtocart.html", context)


class ManageCartView(View):
    def get(self, request, cp_id, act, * args, **kwargs):
        cp = CartProduct.objects.get(id=cp_id)
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
            print("Invalid action")
        # return redirect("/my-cart/")
        return redirect("ecomapp:mycart")
