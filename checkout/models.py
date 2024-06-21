from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

from product.models import ProductVersion

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - Cart'

    @property
    def get_total(self):
        items = self.cart_items.all()
        return sum([item.get_total for item in items])

class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_items')
    product_version = models.ForeignKey(ProductVersion, on_delete=models.CASCADE, related_name='cart_product_versions')
    quantity = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product_version.title} - {self.quantity}'

    @property
    def get_total(self):
        return self.quantity * self.product_version.price


class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billing_addresses')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    phone_number = models.CharField(max_length=20)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='billing_addresses')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class WishlistItem(models.Model):
    user = models.ForeignKey(User, related_name='user_wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVersion, related_name='product_wishlist', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self) -> str:
        return f"Wishlist by {self.user.username} for {self.product.title}-{self.product.id}"
