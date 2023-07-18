from rest_framework import serializers
from django.conf import settings

from auth.models import Account
from users.models import User


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

class AdapterUserPayloadSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    email_verified = serializers.DateTimeField(required=True, write_only=True, source='emailVerified', allow_null=True)
    name = serializers.CharField(required=False, write_only=True, allow_null=True)
    image = serializers.CharField(required=False, write_only=True, allow_null=True)


class AdapterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]
        read_only_fields = ["id", "email"]

class GetUserByIdSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, write_only=True)

class GetUserByAccountSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["provider", "provider_account_id"]
        extra_kwargs = {
            "provider": {
                "required": True,
                "read_only": True,
            },
            "provider_account_id": {
                "required": True,
                "source": "providerAccountId",
                "read_only": True,
            },
        }