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
# from drf_spectacular.openapi import SchemaGeneratorExtension

from checkout.models import WishlistItem, ShoppingCart,CartItem
from checkout.api.serializers import WishlistItemCreateSerializer, WishlistItemListSerializer

from .serializers import ShoppingCartSerializer,CartItemCreateSerializer,CartItemReadSerializer,CartItemDeleteSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from product.models import ProductVersion



# @permission_classes([IsAuthenticated])
# class CartItemCreateAPIView(ListCreateAPIView):
#     serializer_class = CartItemReadSerializer
#     queryset = CartItem.objects.all()
#     # permission_classes = (IsAuthenticated,)

#     def get_serializer_class(self):
#         if self.request.method == 'POST':
#             return CartItemCreateSerializer
#         return super().get_serializer_class()
    
#     def create(self, request, *args, **kwargs):     

#         # print(self.request.user)
#         cart = ShoppingCart.objects.get(user=self.request.user)
#         print(cart.get_total)


#         request.data["cart"] = cart.id
        
#         return super().create(request, *args, **kwargs)


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
    

@extend_schema(
    request=WishlistItemListSerializer,
    responses={200: WishlistItemListSerializer, 400: 'Bad Request', 404: 'Not Found'},   
)
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


@extend_schema(
    request=ShoppingCartSerializer,
    responses={200: ShoppingCartSerializer, 400: 'Bad Request', 404: 'Not Found'},   
)
class CartApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        serializer = ShoppingCartSerializer(cart, context={'request': request})
        return Response(serializer.data)



@extend_schema(
    # request=CartItemReadSerializer,
    responses={201: CartItemReadSerializer, 400: 'Bad Request', 404: 'Not Found'},
    parameters=[
        OpenApiParameter(name='product', type=int, required=True, description='ID of the product to add to the wishlist'),
        OpenApiParameter(name='quantity', type=int, required=True, description='Quantity of the product to add to the wishlist'),

    ]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def AddToCartItemView(request):
    if request.method == 'POST':
        product = request.data.get('product')
        quantity = request.data.get('quantity')
        if not product:
            return JsonResponse({'error': 'Product ID is required'}, status=404)
        if not quantity:
            return JsonResponse({'error': 'Quantity is required'}, status=404)
        
        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        
        try:
            product_version = ProductVersion.objects.get(id=product)
        except ProductVersion.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        
        if cart.cart_items.filter(product_version=product_version).exists():
            cart_item = cart.cart_items.get(product_version=product_version)
            cart_item.quantity += int(quantity)
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart=cart, product_version=product_version, quantity=quantity)
        
        serializer = CartItemReadSerializer(cart_item, context={'request': request})
        return JsonResponse(serializer.data, status=201)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cart_read_del(request, pk):
    cart_item = CartItem.objects.filter(id=pk).first()
    if cart_item:
        if request.method == 'DELETE':
            cart_item.delete()
            return JsonResponse({'message': 'Item is deleted successfully from cart'}, status=204)
    else:
        return JsonResponse({'error': 'Item isnt in your cart'}, status=404)



class IncrementCartItemQuantityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, cart_item_id):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
            cart_item.quantity += 1
            cart_item.save()
            serializer = CartItemReadSerializer(cart_item, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


class DecrementCartItemQuantityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, cart_item_id):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                serializer = CartItemReadSerializer(cart_item, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Quantity cannot be less than 1'}, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)