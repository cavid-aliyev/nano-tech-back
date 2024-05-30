from rest_framework import viewsets
from product.models import Brand, ProductTag, ProductCategory, ProductSubcategory, ProductColor, ProductVersion, ProductVersionImage
from .serializers import BrandSerializer, ProductTagSerializer, ProductCategorySerializer, ProductSubcategorySerializer, ProductColorSerializer, ProductVersionListSerializer, ProductVersionImageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ProductTagViewSet(viewsets.ModelViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductSubcategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductSubcategory.objects.all()
    serializer_class = ProductSubcategorySerializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

class ProductColorViewSet(viewsets.ModelViewSet):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer

class ProductVersionViewSet(viewsets.ModelViewSet):
    queryset = ProductVersion.objects.all()
    serializer_class = ProductVersionListSerializer

class ProductVersionImageViewSet(viewsets.ModelViewSet):
    queryset = ProductVersionImage.objects.all()
    serializer_class = ProductVersionImageSerializer

@api_view(['GET', 'PUT'])
def product_detail(request, slug):
    try:
        product = ProductVersion.objects.get(slug=slug)
    except ProductVersion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductVersionListSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductVersionListSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def purchase_product(request, slug):
    try:
        product = ProductVersion.objects.get(slug=slug)
    except ProductVersion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if product.stock == 0:
        product.is_active = False
        product.save()
        return Response({'error': 'Out of stock'}, status=status.HTTP_400_BAD_REQUEST)

    product.stock -= 1
    product.sales += 1
    product.save()
    return Response({'message': 'Purchase successful'})

@api_view(['GET'])
def top_sales_products(request):
    top_products = ProductVersion.objects.order_by('-sales')[:10]
    serializer = ProductVersionListSerializer(top_products, many=True)
    return Response(serializer.data)