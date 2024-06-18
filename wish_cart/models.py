from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

from product.models import ProductVersion


class WishlistItem(models.Model):
    user = models.ForeignKey(User, related_name='user_wishlist', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVersion, related_name='product_wishlist', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self) -> str:
        return f"Wishlist by {self.user.username} for {self.product.title}-{self.product.id}"
