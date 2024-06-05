from rest_framework import serializers
from product.models import Brand, ProductTag, ProductCategory, ProductSubcategory, ProductColor, ProductVersion, ProductVersionImage, Discount
from decimal import Decimal


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSubcategory
        fields = '__all__'

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [ 'title', 'discount_type', 'value']

class ProductVersionSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer(required=False)
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ProductVersion
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        discount = data.get('discount')
        price = Decimal(str(data.get('price')))  # Convert price to Decimal
        if discount:
            discount_type = discount.get('discount_type')
            value = Decimal(str(discount.get('value')))  # Convert value to Decimal
            if discount_type == 'percent':
                discounted_price = price - (price * (value / Decimal(100)))  # Perform arithmetic with Decimal
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
