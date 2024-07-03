from rest_framework import serializers
from product.models import Brand, ProductTag, ProductCategory, ProductSubcategory, ProductColor, ProductSize, ProductVersion, ProductVersionImage, Discount, Slider
from decimal import Decimal


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title', 'is_active']

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['id', 'title', 'is_active']


class ProductCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['title']


class ProductCategoryListSerializer(serializers.ModelSerializer):
    sub_categories = ProductCategoryCreateSerializer(many=True, source='subcategories')
    class Meta:
        model = ProductCategory
        fields = ['id', 'title', 'is_active', 'sub_categories']   


class ProductSubcategoryListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source = 'category.title')

    class Meta:
        model = ProductSubcategory
        fields = ['id', 'title', 'category']

class ProductSubcategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubcategory
        fields = ['title', 'category']

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'title', 'is_active', "hex_code"]

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [ 'title', 'discount_type', 'value']


class ProductSizeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = (
            'title',
        )

class ProductColorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = (
            'title',
        )

class ProductTagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = (
            'title',
        )

class ProductImagesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersionImage
        fields = ('id', 'image', 'is_active') 



class ProductVersionListSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer(required=False)
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    # color = serializers.CharField(source = 'color.title')
    color = ProductColorListSerializer(many=True)
    size = ProductSizeListSerializer(many=True)
    tags = ProductTagListSerializer(many=True)
    prod_images = ProductImagesListSerializer(many=True, source='images')
    brand = serializers.CharField(source = 'brand.title')
    subcategory = serializers.CharField(source = 'subcategory.title')

    class Meta:
        model = ProductVersion
        fields = ['id','slug', 
                  'title','description',
                  'brand','subcategory','size','color', 'tags',
                    'sales', 'stock', 'is_active', 'price', 'discount', 'discounted_price', 
                    'cover_image', 'prod_images', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        discount = data.get('discount')
        price = Decimal(data.get('price', '0.00'))

        if discount:
            discount_type = discount.get('discount_type')
            value = Decimal(discount.get('value', '0.00'))
            if discount_type == 'percent':
                discounted_price = price - (price * (value / Decimal(100)))
            elif discount_type == 'amount':
                discounted_price = price - value
            data['discounted_price'] = round(discounted_price, 2)
        else:
            data['discounted_price'] = price

        return data
    

class ProductVersionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersionImage
        fields = '__all__'



class ProductVersionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = ['title', 'description', 
                  'brand', 'subcategory', 
                   'price', 'discount', 'stock', 
                  'cover_image']  
    