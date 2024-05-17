from rest_framework import serializers

from blog.models import Blog


class ChangeBlogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "content",
        ]
