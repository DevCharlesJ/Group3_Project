from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.customer_register, name='customer_register'),
    path('login', views.customer_login, name='customer_login'),
    path('logout', views.customer_logout, name='customer_logout'),
    path('about', views.about, name='about'),
    path('cart', views.cart, name='cart'),
    path('products', views.products, name='products'),
    path('products/<int:id>', views.product, name='product'),
    path('products/add_to_cart', views.add_to_cart, name='add_to_cart')
]