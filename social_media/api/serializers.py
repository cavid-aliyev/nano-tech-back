from rest_framework import serializers

from social_media.models import *


class InstagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramProfile
        fields = "__all__"


class FacebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookProfile
        fields = "__all__"


class WhatsappSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsappProfile
        fields = "__all__"


class TelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramProfile
        fields = "__all__"


class TiktokSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiktokProfile
        fields = "__all__"
