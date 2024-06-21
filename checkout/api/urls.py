from django.urls import path
from checkout.api.views import AddToWishlistAPIView, WishlistItemsAPIView, wishlist_read_del

from .views import ShoppingCartAPIView, CartItemCreateAPIView, CartItemDeleteAPIView

app_name = "checkoutapi"
urlpatterns = [
    path('get-wishlist/', WishlistItemsAPIView.as_view(), name='get_wishlist'),
    path('add-to-wishlist/', AddToWishlistAPIView, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:pk>/', wishlist_read_del, name="wishlist_read_del"),

    path('shopping-cart/', ShoppingCartAPIView.as_view(), name='shopping-cart-list-create'),
    path('cart-items/', CartItemCreateAPIView.as_view(), name='cart-item-list-create'),
    path('cart-items/<int:pk>/', CartItemDeleteAPIView.as_view(), name='cart-item-delete-update'),

] 
