from rest_framework import serializers
from product.models import  ProductVersion
from checkout.models import WishlistItem, ShoppingCart, CartItem
from django.contrib.auth import get_user_model

User = get_user_model()

from product.api.serializers import ProductVersionListSerializer, DiscountSerializer,SpecialDiscountSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'get_full_name']


class WishlistProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount = DiscountSerializer(required=False)
    class Meta:
        model = ProductVersion
        fields = ('id', 'title', 'price', 'discount','discounted_price', 'cover_image', 'is_active')
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        discounted_price = instance.get_discounted_price()
        special_discounts = instance.special_discounts.filter(is_active=True).first()
        if special_discounts:
            data['discount'] = SpecialDiscountSerializer(special_discounts).data
            data['discounted_price'] = discounted_price
        if instance.discount:
            data['discounted_price'] = discounted_price
        else:
            data['discount'] = False
        return data


class WishlistItemListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = WishlistProductSerializer()

    class Meta:
        model = WishlistItem
        fields = ('user', 'product')
    


class WishlistItemCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WishlistItem
        fields = (
            'product',
            'user',
        )
        
    def validate(self, attrs):
        attrs["user"] = self.context["request"].user
        return super().validate(attrs)
            



class ShoppingCartforCartItemSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model=ShoppingCart
        fields=(
            'id',
            'user',
        )


class CartItemReadSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    product_version = WishlistProductSerializer()
    cart = ShoppingCartforCartItemSerializer()
    class Meta:
        model=CartItem
        fields=(
            'id',
            'product_version',
            "quantity",
            'cart',
        )
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total'] = instance.get_total
        data['discount_amount'] = instance.get_discount_amount
        data['final_amount'] = instance.get_final_amount
        return data

class CartItemReadforShoppingCartSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    product_version = WishlistProductSerializer()
    class Meta:
        model=CartItem
        fields=(
            'id',
            'product_version',
            "quantity",
        )
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total'] = instance.get_total
        data['discount_amount'] = instance.get_discount_amount
        data['final_amount'] = instance.get_final_amount
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cart__items = CartItemReadforShoppingCartSerializer(many=True, source='cart_items')

    class Meta:
        model=ShoppingCart
        fields=(
            'id',
            'user',
            'cart__items',
        )
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total'] = instance.get_total
        data['discount_amount'] = instance.get_discount_amount
        data['final_amount'] = instance.get_final_amount
        return data


class CartItemCreateSerializer(serializers.ModelSerializer):  
    class Meta:

        model=CartItem
        fields=(
            'id',
            'product_version',
            'quantity',
            'cart',
        )
    def create(self, validated_data):
        print(validated_data["cart"])

        try:
           cart=CartItem.objects.get(cart=validated_data["cart"],product_version=validated_data["product_version"])
           cart.quantity+=validated_data.get("quantity",1)
           cart.save()
           return cart
        except:

          return super().create(validated_data)

class CartItemDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=(
            "quantity",
        )

    def update(self, instance, validated_data):
        quantity_change = validated_data.get('quantity', 0)
        instance.quantity += quantity_change


        if instance.quantity <= 0:
            instance.delete()
            return None
        else:
            instance.save()
            return instance


    