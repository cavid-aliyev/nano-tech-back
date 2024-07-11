from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from blog.models import Blog
from blog.serializers import BlogListSerializer, BlogCreateSerializer, ChangeBlogSerializer


class BlogApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=BlogListSerializer,
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
        serializer = BlogListSerializer(blogs, many=True, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        request=BlogCreateSerializer,
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
        serializer = BlogCreateSerializer(data=request.data)
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


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticatedOrReadOnly])
def blog_detail_view(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response(
            {"message": "Blog not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = BlogListSerializer(blog, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ChangeBlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Blog updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
