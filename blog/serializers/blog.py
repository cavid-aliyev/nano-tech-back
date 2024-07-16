from rest_framework import serializers

from blog.models import Blog, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class BlogListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "subtitle",
            "content",
            "image",
            "category",
            "review_count",
            "created_at",
            "updated_at",
        ]


class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "subtitle",
            "content",
            "image",
            "category",
        ]