from django.urls import path

from .views import *

urlpatterns = [
    path("instagram/", InstagramApiView.as_view(), name="instagram"),
    path("facebook/", FacebookApiView.as_view(), name="facebook"),
    path("whatsapp/", WhatsappApiView.as_view(), name="whatsapp"),
    path("telegram/", TelegramApiView.as_view(), name="telegram"),
    path("tiktok/", TiktokApiView.as_view(), name="tiktok"),
]