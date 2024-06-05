from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status

from blog.models import Blog
from .serializers import BlogSerializer, ChangeBlogSerializer, CategorySerializer


class BlogApiView(APIView):
    serializer_class = BlogSerializer

    @extend_schema(
        request=BlogSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    "description": "Success",
                    "example": {"message": "Success"},
                },
                description="Success",
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
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=BlogSerializer,
        responses={
            201: OpenApiResponse(
                response={
                    "description": "Created",
                    "example": {"message": "Blog created successfully"},
                },
                description="Created",
            ),
            400: OpenApiResponse(
                response={
                    "description": "Bad Request",
                    "example": {"message": "Bad Request"},
                },
                description="Bad Request",
            ),
        },
    )
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=ChangeBlogSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    "description": "Success",
                    "example": {"message": "Blog updated successfully"},
                },
                description="Success",
            ),
            400: OpenApiResponse(
                response={
                    "description": "Bad Request",
                    "example": {"message": "Bad Request"},
                },
                description="Bad Request",
            ),
        },
    )
    def put(self, request):
        id = request.data.get("id")
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return Response(
                {"message": "Blog not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ChangeBlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Blog updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBlogApiView(DestroyAPIView):

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
            {"message": "Blog deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CategoryApiView(CreateAPIView):

    @extend_schema(
        request=CategorySerializer,
        responses={
            201: OpenApiResponse(
                response={
                    "description": "Created",
                    "example": {"message": "Category created successfully"},
                },
                description="Created",
            ),
            400: OpenApiResponse(
                response={
                    "description": "Bad Request",
                    "example": {"message": "Bad Request"},
                },
                description="Bad Request",
            ),
        },
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
