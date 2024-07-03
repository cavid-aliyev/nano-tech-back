from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status

from .serializers import InstagramSerializer, FacebookSerializer, WhatsappSerializer, TelegramSerializer, TiktokSerializer
from social_media.models import InstagramProfile, FacebookProfile, WhatsappProfile, TelegramProfile, TiktokProfile


class InstagramApiView(APIView):
    serializer_class = InstagramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=InstagramSerializer,
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
        instagram_profiles = InstagramProfile.objects.all()
        serializer = InstagramSerializer(instagram_profiles, many=True)
        return Response(serializer.data)
    
class FacebookApiView(APIView):
    serializer_class = FacebookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=FacebookSerializer,
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
        facebook_profiles = FacebookProfile.objects.all()
        serializer = FacebookSerializer(facebook_profiles, many=True)
        return Response(serializer.data)
    
class WhatsappApiView(APIView):
    serializer_class = WhatsappSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=WhatsappSerializer,
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
        whatsapp_profiles = WhatsappProfile.objects.all()
        serializer = WhatsappSerializer(whatsapp_profiles, many=True)
        return Response(serializer.data)
    
class TelegramApiView(APIView):
    serializer_class = TelegramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=TelegramSerializer,
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
        telegram_profiles = TelegramProfile.objects.all()
        serializer = TelegramSerializer(telegram_profiles, many=True)
        return Response(serializer.data)
    
class TiktokApiView(APIView):
    serializer_class = TiktokSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        request=TiktokSerializer,
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
        tiktok_profiles = TiktokProfile.objects.all()
        serializer = TiktokSerializer(tiktok_profiles, many=True)
        return Response(serializer.data)