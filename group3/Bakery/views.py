from django.shortcuts import render, redirect
from .models import *
from .forms import CustomerRegister, CustomerLogin
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse


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


def product(request, id):
    context = {
        'page_name': 'Products',
        'product': Product.objects.get(id, None)
    }
    context.update(load_customer_userdata(request.session))
    
    return render(request, "bakery/product.html", context)


def products(request):
    context = {
        'page_name':'Products',
    }
    context.update(load_customer_userdata(request.session))

    return render(request, 'bakery/products.html', context)


def home(request):
    context = {
        'page_name': 'Home',
    }
    context.update(load_customer_userdata(request.session))
    
    return render(request, 'bakery/index.html', context)