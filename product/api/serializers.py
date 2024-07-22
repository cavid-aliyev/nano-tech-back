from rest_framework import serializers
from product.models import (
        Brand, TopBrand,ProductTag, 
        Category, ProductColor, 
        ProductSize, ProductVersion, ProductVersionImage, 
        Discount, SpecialDiscount, ProductDetail)
from decimal import Decimal
from django.utils import timezone


# class SliderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Slider
#         fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', "image", 'is_active']

class TopBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopBrand
        fields = '__all__'

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['id', 'title', 'is_active']

class ProductTagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['title', 'is_active']


class ProductCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'parent_category']


class CategoryBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title']

class SubcategoryListforCatSerializer(serializers.ModelSerializer):
    brands = CategoryBrandSerializer(many=True)
    class Meta:
        model = Category
        fields = ['id','title', "brands", "is_active", "icon"]


class ProductCategoryListSerializer(serializers.ModelSerializer):
    sub_categories = SubcategoryListforCatSerializer(many=True, source='child_cats')
    brands = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'title', 'sub_categories', "brands", "is_active", "icon"]
        # fields = ['id', 'title', 'is_active']   

    def get_brands(self, obj):
        # Only return brands if the category has no child categories
        if not obj.child_cats.exists():
            return CategoryBrandSerializer(obj.brands.all(), many=True).data
        else:
            brands = set(obj.brands.all())
            for subcategory in obj.child_cats.all():
                brands.update(subcategory.brands.all())
            return CategoryBrandSerializer(brands, many=True).data

class ProductCategoryRetrieveSerializer(serializers.ModelSerializer):
    sub_categories = SubcategoryListforCatSerializer(many=True, source='child_cats')
    brands = serializers.SerializerMethodField()
    main_category = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'title', 'sub_categories', "brands", "main_category", "is_active", "icon"]
        # fields = ['id', 'title', 'is_active']   

    def get_brands(self, obj):
        # Only return brands if the category has no child categories
        if not obj.child_cats.exists():
            return CategoryBrandSerializer(obj.brands.all(), many=True).data
        else:
            brands = set(obj.brands.all())
            for subcategory in obj.child_cats.all():
                brands.update(subcategory.brands.all())
            return CategoryBrandSerializer(brands, many=True).data

    def get_main_category(self, obj):
        if obj.parent_category:
            return ProductCategoryListforSubcatSerializer(Category.objects.filter(title=obj.parent_category.title).first()).data
        return "Main category"
    

class ProductCategoryListforSubcatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', "is_active"]   


# class ProductSubcategoryListSerializer(serializers.ModelSerializer):
#     # category = serializers.CharField(source = 'category.title')
#     category = ProductCategoryListforSubcatSerializer()

#     class Meta:
#         model = ProductSubcategory
#         fields = ['id', 'title', 'category']

# class ProductSubcategoryCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductSubcategory
#         fields = ['title', 'category']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'title', 'is_active', "hex_code"]

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [ 'discount_type', 'value']


class SpecialDiscountSerializer(serializers.ModelSerializer):
    # product = serializers.CharField(source = 'product_version.title')
    class Meta:
        model = SpecialDiscount
        fields = [ 'discount_type', 'value']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     today = timezone.now().date()
    #     if instance.date == today:
    #         representation['is_active'] = True
    #     else:
    #         representation['is_active'] = False
    #     return representation


class ProductSizeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = (
            'id',
            'title',
        )

class ProductColorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = (
            'id',
            'title',
        )

class ProductColorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = (
            'title',
        )

class ProductTagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = (
            'id',
            'title',
        )

class ProductImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersionImage
        fields = ('id', 'image', 'is_active') 

class ProductBrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', "title", 'image']


class ProductDetailSerializer(serializers.ModelSerializer):
    detail_type = serializers.CharField(source = 'detail_type.name')
    class Meta:
        model = ProductDetail
        fields = ( 'id', 'detail_type', 'value')


class ProductCategoryListforProductSerializer(serializers.ModelSerializer):
    # sub_categories = ProductSubcategoryListforCatSerializer(many=True, source='child_cats')
    main_category = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'title',  "main_category"]
    
    def get_main_category(self, obj):
        if obj.parent_category:
            return ProductCategoryListforProductSerializer(Category.objects.filter(title=obj.parent_category.title).first()).data
        return "Main category"


class ProductVersionListSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer(required=False)
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    # color = serializers.CharField(source = 'color.title')
    color = ProductColorListSerializer(many=True)
    size = ProductSizeListSerializer(many=True)
    tags = ProductTagListSerializer(many=True)
    prod_images = ProductImagesListSerializer(many=True, source='images')
    brand = ProductBrandListSerializer()
    # subcategory = serializers.CharField(source = 'subcategory.title')
    category = ProductCategoryListforProductSerializer()
    # special_discount = SpecialDiscountSerializer(source='special_discounts',many=True, read_only=True)
    has_daily_special_discount = serializers.SerializerMethodField()
    product_details = ProductDetailSerializer(source='details', read_only=True, many=True)

    class Meta:
        model = ProductVersion
        fields = ['id','slug', 
                'title','description', 'price', 'discount', 'discounted_price', "has_daily_special_discount",
                'product_details', 
                'brand','category','size','color', 'tags',
                'sales', 'stock', 'is_active', 'is_new',
                'cover_image', 'prod_images', 'created_at', 'updated_at']
    
    def get_has_daily_special_discount(self, obj):
        return obj.has_active_special_discount()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        discounted_price = instance.get_discounted_price()
        # print('discounted_price----------------', discounted_price)
        data['discounted_price'] = discounted_price

        # Check for special discounts first
        # special_discounts = instance.special_discounts.filter(date=timezone.now().date())
        special_discounts = instance.special_discounts.filter(is_active=True).first()
        # if special_discount.exists():
        if special_discounts:
            # special_discount = special_discounts.first()
            data['discount'] = SpecialDiscountSerializer(special_discounts).data
        # elif discount:
        #     data['discounted_price'] = round(discounted_price, 2)
        # else:
        #     data['discounted_price'] = price

        return data
    

class ProductVersionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersionImage
        fields = '__all__'


class ProductVersionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = ['title', 'description', 
                  'brand', 'category', 
                   'price', 'discount', 'stock', 
                  'cover_image']  
    