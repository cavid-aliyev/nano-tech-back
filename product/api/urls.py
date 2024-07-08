from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import ( 
    BrandViewSet, ProductTagViewSet, 
    ProductCategoryViewSet, ProductSubcategoryViewSet, 
    ProductColorViewSet, ProductVersionViewSet, ProductVersionImageViewSet, 
    product_detail, purchase_product,top_sales_products, SliderViewSet, TopBrandViewSet,
    set_language_api, get_language_options_api )

app_name = "product"

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'top-brands', TopBrandViewSet)
router.register(r'tags', ProductTagViewSet)
router.register(r'categories', ProductCategoryViewSet)
router.register(r'subcategories', ProductSubcategoryViewSet)
# router.register(r'products', ProductViewSet)
router.register(r'colors', ProductColorViewSet)
router.register(r'products', ProductVersionViewSet)
router.register(r'product-images', ProductVersionImageViewSet)
router.register(r'sliders', SliderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('product/<slug:slug>/', product_detail, name='product_detail'),
    path('product/<slug:slug>/purchase/', purchase_product, name='purchase_product'),
    # path('top-sales-products/', top_sales_products, name='top_sales_products'),

]