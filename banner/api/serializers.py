from rest_framework import serializers
from banner.models import  Banner


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'description', 'is_active', 'created_at', 'updated_at']