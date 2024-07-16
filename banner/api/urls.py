from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from .views import  BannerViewSet

app_name = "banner"

router_b = DefaultRouter()
router_b.register(r'home-page-banner', BannerViewSet)


urlpatterns = [
    path('', include(router_b.urls))
]