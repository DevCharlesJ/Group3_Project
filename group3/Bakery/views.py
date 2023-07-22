from django.shortcuts import render
from .models import *

# Create your views here.
def login(request):
    # if request.type = "POST"
    # Visitor submitted login data in form

    return render(request, 'bakery/login.html')


def about(request):
    return render(request, 'bakery/about.html', {'page_name': 'About'})


def cart(request):
    return render(request, 'bakery/cart.html')


def product(request, id):
    product = None
    try:
        product=Product.objects.get(id, None)
    except: pass
    
    return render(request, "bakery/product.html", {'product':product})


def products(request):
    return render(request, 'bakery/products.html', {'page_name': 'Products'})


def home(request):
    return render(request, 'bakery/index.html', {'page_name': 'Home'})