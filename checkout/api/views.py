from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,  IsAuthenticatedOrReadOnly,AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from checkout.models import WishlistItem, ShoppingCart,CartItem
from checkout.api.serializers import WishlistItemCreateSerializer, WishlistItemListSerializer

from .serializers import ShoppingCartSerializer,CartItemCreateSerializer,CartItemReadSerializer,CartItemDeleteSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from product.models import ProductVersion



@permission_classes([IsAuthenticatedOrReadOnly])
class ShoppingCartAPIView(ListCreateAPIView):

    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly)


@permission_classes([IsAuthenticated])
class CartItemCreateAPIView(ListCreateAPIView):
    serializer_class = CartItemReadSerializer
    queryset = CartItem.objects.all()
    # permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemCreateSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):     

        # print(self.request.user)
        cart = ShoppingCart.objects.get(user=self.request.user)
        print(cart.get_total)


        request.data["cart"] = cart.id
        
        return super().create(request, *args, **kwargs)


@permission_classes([IsAuthenticated])
class CartItemDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemDeleteSerializer
    queryset = CartItem.objects.all()
    # permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):

        return super().destroy(request, *args, **kwargs)



@extend_schema(
    request=WishlistItemCreateSerializer,
    responses={201: WishlistItemCreateSerializer, 400: 'Bad Request', 404: 'Not Found'},
    parameters=[
        OpenApiParameter(
            name='product',
            type=int,
            required=True,
            description='ID of the product to add to the wishlist'
        )
    ]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def AddToWishlistAPIView(request):
    serializer = WishlistItemCreateSerializer(data=request.data, context = {'request':request})
    product = request.data.get('product')
    if not product:
        return JsonResponse({'error': 'Product ID is required'}, status=404)
    

    #  Check if the product already exists in the user's wishlist
    if request.user.user_wishlist.filter(product__id=product).exists():
        return JsonResponse({'error': 'Product already exists in wishlist'}, status=400)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status = 201)
    return JsonResponse(serializer.errors, status = 400)
    

class WishlistItemsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # queryset = WishlistItem.objects.all()
    def get(self, request):
        wishlist_items = WishlistItem.objects.filter(user=request.user)
        serializer = WishlistItemListSerializer(wishlist_items,  context = {'request':request}, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def wishlist_read_del(request, pk):
    wishlist = WishlistItem.objects.filter(product_id=pk, user = request.user).first()
    # print(wishlist)

    if wishlist:
        if request.method == 'DELETE':
            wishlist.delete()
            return JsonResponse({'message': 'Product is deleted successfully from wishlist'}, status=204)
    else:    
        return JsonResponse({'error': 'Product isnt in your wishlist'}, status=404)


