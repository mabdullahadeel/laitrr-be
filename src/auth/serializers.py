from rest_framework import serializers
from django.conf import settings


class SocialAuthResponseSerializer(serializers.Serializer):
    authorization_url = serializers.CharField(read_only=True)


class SocialAuthQueryParamValidationSerializer(serializers.Serializer):
    redirect_url = serializers.URLField(required=True, write_only=True)
    provider = serializers.ChoiceField(
        required=True,
        write_only=True,
        choices=["google-oauth2"],
    )

    def validate(self, attrs: dict):
        redirect_url: str = attrs.get("redirect_url")
        provider: str = attrs.get("provider")
        if redirect_url not in getattr(settings, "ALLOWED_REDIRECT_URLS", []):
            raise serializers.ValidationError("redirect_url is not allowed")
        if provider not in getattr(settings, "ALLOWED_AUTH_PROVIDERS", []):
            raise serializers.ValidationError("provider is not allowed")

        return super().validate(attrs)
