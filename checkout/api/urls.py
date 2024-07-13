from django.urls import path
from checkout.api.views import AddToWishlistAPIView, WishlistItemsAPIView, wishlist_read_del, CartApiView, AddToCartItemView, cart_read_del

from .views import CartItemDeleteAPIView

app_name = "checkoutapi"
urlpatterns = [
    path('get-wishlist/', WishlistItemsAPIView.as_view(), name='get_wishlist'),
    path('add-to-wishlist/', AddToWishlistAPIView, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:pk>/', wishlist_read_del, name="wishlist_read_del"),

    # path('get-shopping-cart/', ShoppingCartAPIView.as_view(), name='shopping-cart-list-create'),
    # path('add-to-cart/', CartItemCreateAPIView.as_view(), name='cart-item-list-create'),
    # path('delete-from-cart/<int:pk>/', CartItemDeleteAPIView.as_view(), name='cart-item-delete-update'),

    path('get-shopping-cart/', CartApiView.as_view(), name='get-shopping-cart'),
    path('add-to-cart/', AddToCartItemView, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', cart_read_del, name='cart-item-delete'),
] 
