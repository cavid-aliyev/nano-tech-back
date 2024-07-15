from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from home.api.views import SliderViewSet, BannerViewSet

app_name = "home"

router = DefaultRouter()
router.register(r'sliders', SliderViewSet)
router.register(r'home-page-banner', BannerViewSet)


urlpatterns = [
    path('', include(router.urls))
]