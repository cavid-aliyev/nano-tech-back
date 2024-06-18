from rest_framework import serializers
from product.models import  ProductVersion
from wish_cart.models import WishlistItem
from django.contrib.auth import get_user_model

User = get_user_model()



class WishlistProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVersion
        fields = ('id', 'title', 'price', 'cover_image', 'is_active')


class WishlistItemListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = 'user.username')
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
            
            
    