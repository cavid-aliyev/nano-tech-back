from rest_framework import serializers

from blog.models import Blog, Category


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
            "category",
            "review_count",
            "created_at",
            "updated_at",
        ]


class ChangeBlogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]