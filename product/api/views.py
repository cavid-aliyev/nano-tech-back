from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.http import JsonResponse
from django.utils import translation
from django.utils.translation import get_language_info
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from product.models import (Brand, TopBrand, 
    ProductTag, ProductCategory, ProductSubcategory, 
    ProductColor, ProductVersion, ProductVersionImage, Slider)
from .serializers import ( 
    BrandSerializer, ProductTagSerializer, ProductTagCreateSerializer, 
    ProductCategoryListSerializer, ProductCategoryCreateSerializer, 
    ProductSubcategoryListSerializer,ProductSubcategoryCreateSerializer, 
    ProductColorSerializer, ProductColorCreateSerializer,
    ProductVersionListSerializer, ProductVersionCreateSerializer, ProductVersionImageSerializer, 
    SliderSerializer, TopBrandSerializer)
from product.filters import ProductVersionFilter

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def set_language_api(request):
    """
    API endpoint to set the language for the current session.
    """
    lang_code = request.data.get('language')

    # Check if the provided language code is valid
    if lang_code and lang_code in dict(settings.LANGUAGES).keys():
        # Activate the specified language
        translation.activate(lang_code)

        # Update session variables
        request.session[settings.LANGUAGE_SESSION_KEY] = lang_code
        request.session[settings.LANGUAGE_CODE] = lang_code

        return JsonResponse({'status': 'success', 'message': f'Language changed to {lang_code}'})
    else:
        return JsonResponse({'status': 'failure', 'message': 'Invalid language code'}, status=400)


def get_language_options():
    # Get the current language
    current_language = translation.get_language()

    # Get available languages
    available_languages = settings.LANGUAGES

    # Generate the list of languages with selection status
    languages_info = []
    for lang_code, lang_name in available_languages:
        language_info = get_language_info(lang_code)
        language_info['selected'] = lang_code == current_language
        languages_info.append(language_info)
    
    return languages_info


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="List of available languages",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'languages': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'code': openapi.Schema(type=openapi.TYPE_STRING),
                                'name': openapi.Schema(type=openapi.TYPE_STRING),
                                'bidi': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'name_local': openapi.Schema(type=openapi.TYPE_STRING),
                                'name_translated': openapi.Schema(type=openapi.TYPE_STRING),
                                'selected': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            }
                        )
                    )
                }
            )
        )
    },
    operation_summary="Get available languages"
)
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_language_options_api(request):
    """
    API endpoint to get the list of available languages.
    """
    languages_info = get_language_options()
    return JsonResponse({'languages': languages_info})


@permission_classes([IsAuthenticatedOrReadOnly])
class SliderViewSet(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer

@permission_classes([IsAuthenticatedOrReadOnly])
class TopBrandViewSet(viewsets.ModelViewSet):
    queryset = TopBrand.objects.all()
    serializer_class = TopBrandSerializer


@permission_classes([IsAuthenticatedOrReadOnly])
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

@permission_classes([IsAuthenticatedOrReadOnly])
class ProductTagViewSet(viewsets.ModelViewSet):
    queryset = ProductTag.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductTagSerializer
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return  ProductTagCreateSerializer
        return ProductTagSerializer  # default serializer


@permission_classes([IsAuthenticatedOrReadOnly])
class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductCategoryListSerializer
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return  ProductCategoryCreateSerializer
        return ProductCategoryListSerializer  # default serializer


@permission_classes([IsAuthenticatedOrReadOnly])
class ProductSubcategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductSubcategory.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductSubcategoryListSerializer
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return  ProductSubcategoryCreateSerializer
        return ProductSubcategoryListSerializer  # default serializer

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

@permission_classes([IsAuthenticatedOrReadOnly])
class ProductColorViewSet(viewsets.ModelViewSet):
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorSerializer

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductColorSerializer
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return  ProductColorCreateSerializer
        return ProductColorSerializer  # default serializer
    



@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter( name='is_new', type=bool, required=False,enum=[True, False], description='Filter products that are new'),
            OpenApiParameter( name='discount', description='Filter by profitable products (products with a discount or daily special discount)', required=False, type=bool, enum=[True]),
            OpenApiParameter(name='daily_special_discount', description='Filter product with daily special discounts (only one product with daily discount last added )', required=False, type=bool, enum=[True]),
            OpenApiParameter( name='top_sales', description='Filter by top sales products (products with sales > 0, descending order by sales)', required=False,type=bool, enum=[True]),
            OpenApiParameter( name='min_price', type=OpenApiTypes.INT, required=False,  description='Filter products with a minimum price'),
            OpenApiParameter( name='max_price', type=OpenApiTypes.INT, required=False, description='Filter products with a maximum price'),
            OpenApiParameter( name='search', description='Search in title and description', required=False, type=str),
            OpenApiParameter(name='page', type=OpenApiTypes.INT, required=False, description='A page number within the paginated result set'),
            OpenApiParameter(name='page_size', type=OpenApiTypes.INT, required=False, description='Number of items per page'),
            OpenApiParameter(name='brand_id', type=OpenApiTypes.INT, required=False, description='Filter products by brand ID'),
            OpenApiParameter(name='category_id', type=OpenApiTypes.INT, required=False, description='Filter products by category ID'),
       ]
    )
)
@permission_classes([IsAuthenticatedOrReadOnly])
class ProductVersionViewSet(viewsets.ModelViewSet):
    queryset = ProductVersion.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductVersionFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'dis_price']  # Allow ordering by price

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductVersionListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ProductVersionCreateSerializer
        return ProductVersionListSerializer  # default serializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        filterset = self.filterset_class(request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        start = (page - 1) * page_size
        end = start + page_size

        paginated_queryset = queryset[start:end]
        serializer = self.get_serializer(paginated_queryset, many=True)
        return Response(serializer.data)



@permission_classes([IsAuthenticatedOrReadOnly])
class ProductVersionImageViewSet(viewsets.ModelViewSet):
    queryset = ProductVersionImage.objects.all()
    serializer_class = ProductVersionImageSerializer




@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_detail(request, slug):
    try:
        product = ProductVersion.objects.get(slug=slug)
    except ProductVersion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Serialize the main product
        serializer = ProductVersionListSerializer(product)
        data = serializer.data

        # Fetch similar products (same category, excluding the current product)
        similar_products = ProductVersion.objects.filter(subcategory__category=product.subcategory.category).exclude(slug=product.slug)
        similar_serializer = ProductVersionListSerializer(similar_products, many=True)
        data['similar_products'] = similar_serializer.data

        return Response(data)

    elif request.method == 'PUT':
        serializer = ProductVersionListSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
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
@permission_classes([IsAuthenticatedOrReadOnly])
def top_sales_products(request):
    top_products = ProductVersion.objects.order_by('-sales')[:10]
    serializer = ProductVersionListSerializer(top_products, many=True)
    return Response(serializer.data)