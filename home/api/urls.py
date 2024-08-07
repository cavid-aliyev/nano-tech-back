from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter
from home.api.views import SliderViewSet

app_name = "home"

router = DefaultRouter()
router.register(r'sliders', SliderViewSet)


urlpatterns = [
    path('', include(router.urls))
]