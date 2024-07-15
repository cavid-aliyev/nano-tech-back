from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


from home.models import Slider, Banner
from home.api.serializers import SliderSerializer, BannerSerializer


@permission_classes([IsAuthenticatedOrReadOnly])
class SliderViewSet(viewsets.ModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer


@permission_classes([IsAuthenticatedOrReadOnly])
class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


