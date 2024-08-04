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
from django.db.models import QuerySet

from product.models import (Brand, TopBrand, 
    ProductTag, Category, ProductDetail, ProductDetailType,
    ProductColor, ProductVersion, ProductVersionImage)
from .serializers import ( 
    BrandSerializer, ProductTagSerializer, ProductTagCreateSerializer, 
    ProductCategoryListSerializer, ProductCategoryCreateSerializer, ProductCategoryRetrieveSerializer,
    # ProductSubcategoryListSerializer,ProductSubcategoryCreateSerializer, 
    ProductColorSerializer, ProductColorCreateSerializer,
    ProductVersionListSerializer, ProductVersionCreateSerializer, ProductVersionImageSerializer, 
    TopBrandSerializer, FilterOptionsSerializer)
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
        # language_info['selected'] = lang_code == current_language
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
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductCategoryListSerializer
        if self.action == 'retrieve':
            return ProductCategoryRetrieveSerializer
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return  ProductCategoryCreateSerializer
        return ProductCategoryListSerializer  # default serializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            categories = Category.objects.filter(parent_category=None)
            return categories
        return queryset


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
            OpenApiParameter( name='is_new', type=bool, required=False,enum=[True], description='Filter products that are new'),
            OpenApiParameter( name='discount', description='Filter by profitable products (products with a discount or daily special discount)', required=False, type=bool, enum=[True]),
            OpenApiParameter(name='daily_special_discount', description='Filter product with daily special discounts (only one product with daily discount last added )', required=False, type=bool, enum=[True]),
            OpenApiParameter( name='top_sales', description='Filter by top sales products (products with sales > 0, descending order by sales)', required=False,type=bool, enum=[True]),
            OpenApiParameter( name='min_price', type=OpenApiTypes.INT, required=False,  description='Filter products with a minimum price'),
            OpenApiParameter( name='max_price', type=OpenApiTypes.INT, required=False, description='Filter products with a maximum price'),
            OpenApiParameter( name='search', description='Search in title and description', required=False, type=str),
            OpenApiParameter(name='page', type=OpenApiTypes.INT, required=False, description='A page number within the paginated result set'),
            OpenApiParameter(name='page_size', type=OpenApiTypes.INT, required=False, description='Number of items per page'),
            OpenApiParameter(name='brand_id', type=OpenApiTypes.INT, required=False, description='Filter products by brand ID (comma-separated list like brand_id=1,2,3)'),
            OpenApiParameter(name='category_id', type=OpenApiTypes.INT, required=False, description='Filter products by category ID (comma-separated list like category_id=1,2,3)'),
            OpenApiParameter(name='order_by', type=OpenApiTypes.STR, enum=['-price', 'price','newest', 'title'], required=False, description='Order products by price(price: ascending, -price:descending), newest, or title'),
       ]
    )
)
@permission_classes([IsAuthenticatedOrReadOnly])
class ProductVersionViewSet(viewsets.ModelViewSet):
    queryset = ProductVersion.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_class = ProductVersionFilter
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductVersionListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ProductVersionCreateSerializer
        return ProductVersionListSerializer  # default serializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'retrieve':
            return queryset
        
        queryset = self.filter_queryset(queryset)

        is_new = self.request.query_params.get('is_new')
        top_sales = self.request.query_params.get('top_sales', None)
        discount = self.request.query_params.get('discount', None)
        daily_special_discount = self.request.query_params.get('daily_special_discount', None)
        ordering = self.request.query_params.get('order_by')
        max_price = self.request.query_params.get('max_price')
        min_price = self.request.query_params.get('min_price')
        brand_ids = self.request.query_params.get('brand_id')
        category_ids = self.request.query_params.get('category_id')
        # processor = self.request.query_params.get('processor')

        products = list(queryset)

        if ordering == "price" or ordering == "-price" or ordering == "newest" or ordering == "title":
            if ordering == "price":  # evvelce ucuz
                # Fetch all products and sort them in Python
                products.sort(key=lambda product: product.get_discounted_price())
            elif ordering == "-price":  # evvelce bahali
                products.sort(key=lambda product: product.get_discounted_price(), reverse=True)
            elif ordering == "newest":  # en yeniler
                products.sort(key=lambda product: product.created_at, reverse=True)
            elif ordering == "title":  # mehsulun adina gore
                products.sort(key=lambda product: product.title)
        if max_price:
            products = [product for product in products if product.get_discounted_price() <= int(max_price)]
        if min_price:
            products = [product for product in products if product.get_discounted_price() >= int(min_price)]
        if is_new:
            products = [product for product in products if product.is_new]
        if top_sales == "true" or top_sales == "True":
            products = [product for product in products if product.sales > 0]
            products.sort(key=lambda product: product.sales, reverse=True)
        if discount == "true" or discount == "True":
            products = [product for product in products if product.discount or product.special_discounts.filter(is_active=True).exists()]
        if daily_special_discount == "true" or daily_special_discount == "True":
            products = [product for product in products if product.special_discounts.filter(is_active=True).exists()]
            products.sort(key=lambda product: product.special_discounts.filter(is_active=True).last().created_at, reverse=True)
            products = products[:1]
        if brand_ids:
            brand_ids = list(map(int, brand_ids.split(',')))  # Convert comma-separated string to a list of integers
            # print(brand_ids, "brand_ids------")
            products = [product for product in products if product.brand.id in brand_ids]
        if category_ids:
            category_ids = list(map(int, category_ids.split(',')))
            print(category_ids, "category_ids------")

            filtered_products = []
            for product in products:
                # Include products from the specified categories
                if product.category.id in category_ids:
                    filtered_products.append(product)
                
                # Include products from subcategories of the specified main categories
                if product.category.parent_category and product.category.parent_category.id in category_ids:
                    filtered_products.append(product)
        
            products = filtered_products
        # if processor:
        #     processor_titles = list(map(str, processor.split(',')))
        #     print(processor_titles, "processor_titles------")
        #     products = [product for product in products if product.details in processor_titles]
            
        
        return products
        # return queryset.filter(pk__in=[product.pk for product in products])
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Fetch similar products (example logic, modify as needed)
        similar_products = ProductVersion.objects.filter(
            category=instance.category
        ).exclude(id=instance.id)  # Fetch the top 3 similar products
        
        response_data = serializer.data
        if similar_products:
            similar_products_serializer = ProductVersionListSerializer(similar_products, many=True)
            response_data['similar_products'] = similar_products_serializer.data
        else:
            response_data['similar_products'] = []

        return Response(response_data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 12))
        start = (page - 1) * page_size
        end = start + page_size
        paginated_queryset = queryset[start:end]
        serializer = self.get_serializer(paginated_queryset, many=True)

        categories = list(Category.objects.filter(product_versions__in=queryset).distinct().values('id', 'title'))
        brands = list(Brand.objects.filter(product_versions__in=queryset).distinct().values('id', 'title'))
        tags = list(ProductTag.objects.filter(product_tags__in=queryset).distinct().values('id', 'title'))
        colors = list(ProductColor.objects.filter(product_verions__in=queryset).distinct().values('id', 'title'))
        
        # Fetch and aggregate distinct detail types
        raw_details = ProductDetail.objects.filter(product__in=queryset).values('detail_type__id', 'detail_type__name')
        details = []
        seen = set()
        for detail in raw_details:
            detail_type_id = detail['detail_type__id']
            detail_type_name = detail['detail_type__name']
            if (detail_type_id, detail_type_name) not in seen:
                seen.add((detail_type_id, detail_type_name))
                details.append({
                    'detail_type__id': detail_type_id,
                    'detail_type__name': detail_type_name
                })

        filter_options = {
            'categories': categories,
            'brands': brands,
            'colors': colors,
            'tags': tags,
            'details': details,
        }

        response_data = {
            'products': serializer.data,
            'filters': filter_options,
        }

        # return Response(serializer.data)
        return Response(response_data)
    



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
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'Product not found'})

    if request.method == 'GET':
        # Serialize the main product
        serializer = ProductVersionListSerializer(product, context={'request': request})
        data = serializer.data

        # Fetch similar products (same category, excluding the current product)
        similar_products = ProductVersion.objects.filter(category=product.category).exclude(slug=product.slug)
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