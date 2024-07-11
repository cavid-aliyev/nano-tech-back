from rest_framework import serializers

from blog.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
            "image",
            "category",
            "review_count",
            "created_at",
            "updated_at",
        ]
