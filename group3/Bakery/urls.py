from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('about', views.about, name='about'),
    path('cart', views.cart, name='cart'),
    path('products', views.products, name='products'),
    path('products/<int:id>', views.product, name='product'),
]