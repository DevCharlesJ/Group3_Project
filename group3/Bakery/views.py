from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import CustomerRegister, CustomerLogin
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse

import os

this_dir = os.path.dirname(__file__)

# Obtain user data fir customers
def load_customer_userdata(session) -> dict:
    customer_id = session.get('customer_id', None)
    return {
        'user': Customer.objects.get(id=customer_id) if customer_id is not None else None
    }



# Create your views here.
def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegister(request.POST)
        if form.is_valid():
            try:
                form.save(commit=True)
                redirect(reverse('customer_login'))
            except IntegrityError:
                form.add_error('email', 'This email already exists!')
    else:
        form = CustomerRegister()

    return render(request, 'registration/customer_register.html', {'form': form})


def customer_login(request):
    error = ""
    if request.method == 'POST':
        form = CustomerLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            customer = authenticate(request, email=email, password=password)
            if customer:
                # Assign shopping cart (if not existing)
                try:
                    cart = Shopping_Cart.objects.get(customer=customer)
                except:
                    cart = Shopping_Cart(
                        id=Shopping_Cart.objects.count(), 
                        customer = customer
                    )

                    cart.save()

                auth_login(request, customer)

                # Cachine is not working properly
                # Explicitely set customer_id to session
                request.session['customer_id'] = customer.id
                
                return redirect(reverse('home'))

            error = "Incorrect email or password"
    else:
        form = CustomerLogin()

    return render(request, 'registration/customer_login.html', {'form': form, 'login_error': error})

def customer_logout(request):
    request.session['customer_id'] = None
    return redirect(reverse('home'))

def about(request):
    context = {
        'page_name': 'About',
    }
    context.update(load_customer_userdata(request.session))

    about_info_file = os.path.join(this_dir, "static/textfiles/aboutinfo.txt")
    with open(about_info_file, "r") as f:
        context['about_document'] = f.readlines()

    return render(request, 'bakery/about.html', context)




def cart(request):
    context = {
        'page_name': 'Cart',
    }
    context.update(load_customer_userdata(request.session))
    if context.get('user', None) is not None:
        return render(request, 'bakery/cart.html', context)
    else:
        # User is not logged in
        return redirect(reverse('customer_login'))
    
def add_product_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        context = {}
        context.update(load_customer_userdata(request.session))


        if product_id is not None and context['user'] is not None:
            customer:Customer = context['user']
            try:
                cart:Shopping_Cart = Shopping_Cart.objects.get(customer=customer)
            except:
                return HttpResponse("Shopping cart not found", status=400)
            
            try:
                product = Product.objects.get(id=product_id)
            except:
                return HttpResponse("Product not found", status=400)

            try:
                # Check if shopping item exists
                shopping_item  = Shopping_Item.objects.get(shopping_cart=cart, product=product)
                shopping_item.increaseQuantityBy(1) # accumulate quantity by 1
            except:
                # Create new shopping item
                shopping_item = Shopping_Item(shopping_cart=cart, product=product)

            print(shopping_item.getCollectiveCost())
                

            return HttpResponse("OK", status=200)
        
        return HttpResponse("Error processing request", status=400)




def product(request, id):
    context = {
        'page_name': 'Products',
        'product': Product.objects.get(id=id)
    }
    context.update(load_customer_userdata(request.session))
    
    return render(request, "bakery/product.html", context)


def products(request):
    context = {
        'page_name':'Products',
        'products': {} # Keys: Product type (name), Val: list[Products]
    }

    # Map a list of products of certain types
    for product in Product.objects.all():
        pt_name = product.product_type.name
        
        # This appends will append the product to the list of product type
        context["products"][pt_name] = context["products"].get(pt_name, []) + [product]

    context.update(load_customer_userdata(request.session))

    return render(request, 'bakery/products.html', context)


def home(request):
    context = {
        'page_name': 'Home',
    }
    context.update(load_customer_userdata(request.session))

    news_file = os.path.join(this_dir, "static/textfiles/news.txt")
    with open(news_file, "r") as f:
        context['news_document'] = f.readlines()

    
    return render(request, 'bakery/index.html', context)