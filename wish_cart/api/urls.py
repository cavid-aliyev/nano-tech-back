from django.urls import path
from wish_cart.api.views import AddToWishlistAPIView, WishlistItemsAPIView, wishlist_read_del


app_name = "checkoutapi"
urlpatterns = [
    path('get-wishlist/', WishlistItemsAPIView.as_view(), name='get_wishlist'),
    path('add-to-wishlist/', AddToWishlistAPIView, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:pk>/', wishlist_read_del, name="wishlist_read_del"),

] 
