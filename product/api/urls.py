from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, ProductTagViewSet, ProductCategoryViewSet, ProductSubcategoryViewSet, ProductColorViewSet, ProductVersionViewSet, ProductVersionImageViewSet, product_detail, purchase_product,top_sales_products

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'product-tags', ProductTagViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'product-subcategories', ProductSubcategoryViewSet)
# router.register(r'products', ProductViewSet)
router.register(r'product-colors', ProductColorViewSet)
router.register(r'product-versions', ProductVersionViewSet)
router.register(r'product-version-images', ProductVersionImageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('products/<slug:slug>/', product_detail, name='product_detail'),
    path('products/<slug:slug>/purchase/', purchase_product, name='purchase_product'),
    path('top-sales-products/', top_sales_products, name='top_sales_products'),
]