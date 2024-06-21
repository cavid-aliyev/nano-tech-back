from django.urls import path
from .views import ShoppingCartAPIView, CartItemCreateAPIView, CartItemDeleteAPIView

urlpatterns = [
    path('shopping-cart/', ShoppingCartAPIView.as_view(), name='shopping-cart-list-create'),
    path('cart-items/', CartItemCreateAPIView.as_view(), name='cart-item-list-create'),
    path('cart-items/<int:pk>/', CartItemDeleteAPIView.as_view(), name='cart-item-delete-update'),
]
