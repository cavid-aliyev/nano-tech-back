from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

from blog.models import Blog
from blog.serializers import BlogListSerializer,BlogCreateSerializer, ChangeBlogSerializer


class DeleteBlogApiView(DestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=ChangeBlogSerializer,
        responses={
            204: OpenApiResponse(
                response={
                    "description": "No Content",
                    "example": {"message": "Blog deleted successfully"},
                },
                description="No Content",
            ),
            400: OpenApiResponse(
                response={
                    "description": "Bad Request",
                    "example": {"message": "Bad Request"},
                },
                description="Bad Request",
            ),
            404: OpenApiResponse(
                response={
                    "description": "Not Found",
                    "example": {"message": "Not Found"},
                },
                description="Not Found",
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        try:
            blog = Blog.objects.get(id=kwargs.get("pk"))
        except Blog.DoesNotExist:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        blog.delete()
        return Response(
            {"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )
