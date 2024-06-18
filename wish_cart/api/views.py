from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from drf_spectacular.utils import extend_schema

from wish_cart.models import WishlistItem
from wish_cart.api.serializers import WishlistItemCreateSerializer, WishlistItemListSerializer


@extend_schema(
    # request={
    #     "type": "object",
    #     "properties": {
    #         "product": {"type": "integer"}
    #     },
    #     "required": ["product"]
    # },
    # responses={
    #     201: WishlistItemCreateSerializer,
    #     400: {"error": {"type": "string"}}
    # },
    description="Add a product to the user's wishlist, with bearer token, and product id as 'product",
    
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def AddToWishlistAPIView(request):
    serializer = WishlistItemCreateSerializer(data=request.data, context = {'request':request})
    product = request.data.get('product')
    if not product:
        return JsonResponse({'error': 'Product ID is required'}, status=404)
    

    # Check if the product already exists in the user's wishlist
    wishlist = request.user.user_wishlist.all()
    if wishlist.filter(product__id=product).exists():
        return JsonResponse({'error': 'Product already exists in wishlist'}, status=404)
    else:
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


