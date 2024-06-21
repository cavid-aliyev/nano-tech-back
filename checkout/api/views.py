from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly,AllowAny
from .serializers import ShoppingCartSerializer,CartItemCreateSerializer,CartItemReadSerializer,CartItemDeleteSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from checkout.models import ShoppingCart,CartItem
from product.models import ProductVersion




class ShoppingCartAPIView(ListCreateAPIView):

    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly)


class CartItemCreateAPIView(ListCreateAPIView):
    serializer_class = CartItemReadSerializer
    queryset = CartItem.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):

        print(self.request.user)
        cart = ShoppingCart.objects.get(user=self.request.user)
        print(cart.get_total)
        

        request.data["cart"] = cart.id
        
        return super().create(request, *args, **kwargs)


class CartItemDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemDeleteSerializer
    queryset = CartItem.objects.all()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):

        return super().destroy(request, *args, **kwargs)
