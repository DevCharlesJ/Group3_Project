from django.db import models
from django.core.validators import MinValueValidator

# SETTER AND GETTER METHODS ARE AUTOMATICALLY CREATED
# DON'T HAVE TO IMPLEMENT, UNLESS ADDITIONAL FUNCTIONALITY IS NEEDED

class Product_Type(models.Model):
    # All product types must have unique names
    name = models.CharField(max_length=80, primary_key=True)

class Product(models.Model):
    id = models.IntegerField(primary_key=True)

    # Each product can only refer to zero or 1 product type
    product_type = models.OneToOneField(Product_Type, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=350, null=True)
    price = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )
    

class Customer(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=80, primary_key=True)
    password = models.CharField(max_length=80)

    def getCart():
        """Returns shopping cart"""
        pass


class Shopping_Cart(models.Model):
    id = models.IntegerField(primary_key=True)

    # A shopping car must belong to at most 1 customer
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, db_column='email')

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



