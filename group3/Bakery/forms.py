from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegister(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email')

class CustomerLogin(forms.Form):
    email = forms.CharField(max_length=80, required=True)
    password = forms.CharField(max_length=80, required=True, widget=forms.PasswordInput)