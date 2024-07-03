from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from blog.models import Blog
from blog.serializers import BlogSerializer, ChangeBlogSerializer


class BlogApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

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
