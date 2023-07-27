from django.contrib.auth.backends import ModelBackend
from .models import Customer


class CustomerBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None
        else:
            if customer.check_password(password):
                return customer
        return None