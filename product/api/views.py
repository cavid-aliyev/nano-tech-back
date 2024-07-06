from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.http import JsonResponse
from django.utils import translation
from django.utils.translation import get_language_info
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticatedOrReadOnly

from product.models import Brand, TopBrand, ProductTag, ProductCategory, ProductSubcategory, ProductColor, ProductVersion, ProductVersionImage, Slider
from .serializers import ( 
    BrandSerializer, ProductTagSerializer, 
    ProductCategoryListSerializer, ProductCategoryCreateSerializer, 
    ProductSubcategoryListSerializer,ProductSubcategoryCreateSerializer, 
    ProductColorSerializer, 
    ProductVersionListSerializer, ProductVersionCreateSerializer, ProductVersionImageSerializer, 
    SliderSerializer, TopBrandSerializer)


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
    serializer_class = ProductTagSerializer


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


@permission_classes([IsAuthenticatedOrReadOnly])
class ProductVersionViewSet(viewsets.ModelViewSet):
    queryset = ProductVersion.objects.all()
    # serializer_class = ProductVersionListSerializer

    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['title', 'description']
    # search_fields = ['title', 'subcategory__title', 'brand__title', 'description']   # ?search=new

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']   # ?search=new

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductVersionListSerializer
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return ProductVersionCreateSerializer
        return ProductVersionListSerializer  # default serializer


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
        serializer = ProductVersionListSerializer(product)
        return Response(serializer.data)

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