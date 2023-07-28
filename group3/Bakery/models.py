from django.db import models
from django.core.validators import MinValueValidator


from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
)

class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email address is required')
        customer = self.model(email=self.normalize_email(email), **kwargs)
        customer.set_password(password)
        customer.save()
        return customer

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, password, **kwargs)

class Customer(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(primary_key=True, default=0)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name='customer_set', verbose_name='groups')

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    objects = CustomerManager()

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customer_user_permissions'
    )

    def __str__(self):
        return self.email
    


# SETTER AND GETTER METHODS ARE AUTOMATICALLY CREATED
# DON'T HAVE TO IMPLEMENT, UNLESS ADDITIONAL FUNCTIONALITY IS NEEDED

class Product_Type(models.Model):
    # All product types must have unique names
    name = models.CharField(max_length=80, primary_key=True)

class Product(models.Model):
    id = models.IntegerField(primary_key=True, default=0)

    # Each product can only refer to zero or 1 product type
    product_type = models.OneToOneField(Product_Type, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=350, null=True)
    price = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )



class Shopping_Cart(models.Model):
    id = models.IntegerField(primary_key=True, default=0)

    # A shopping car must belong to at most 1 customer
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, db_column='customer_id')
    
    def getTotal(self) -> float:
        # need to query shopping items and sum all collective costs
        # sum([item.getCollectiveCost() for item in self.getItems()])?
        pass

    def getItem(self, item):
        pass

    def addItem(self, item):
        pass

    def removeItem(self, item) -> bool:
        pass

    def clearItems(self):
        pass

    def getItems() -> list:
        pass


class Shopping_Item(models.Model):

    # Each shopping item must belong to at most 1 shopping cart
    shopping_cart = models.OneToOneField(Shopping_Cart, related_name="shopping_cart", on_delete=models.CASCADE)
    
    # It shopping item must refer to at most 1 product
    product = models.OneToOneField(Product, related_name="product", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    # Max_quantity?

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['shopping_cart', 'product'], name='unique_shopping_cart_product_combination'
            )
        ]


    def increaseQuantityBy(self, amt):
        self.quantity += amt

    def decreaseQuantityBy(self, amt):
        self.quantity -= max(amt, 0) # ensures quantity is at least 0

    def getCollectiveCost(self):
        base_price = 0 
        try:
            base_price = self.product.price # product could be null
        except:
            return 0

        return base_price*(self.quantity or 0)
    
    def resetQuantity(self):
        self.quantity = 0



