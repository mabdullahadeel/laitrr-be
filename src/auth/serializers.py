from django.utils.crypto import get_random_string
from rest_framework import serializers
from django.conf import settings

from auth.models import Account
from users.models import User, Profile


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


class AdapterUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, write_only=True, allow_null=True)
    image = serializers.URLField(required=False, allow_null=True)
    emailVerified = serializers.DateTimeField(required=False, allow_null=True, source="email_verified")
    
    class Meta:
        model = User
        fields = ["id", "email", "emailVerified", "name", "image"]
        
    def get_names_pair(self, name: str) -> tuple[str, str]:
        return (name.split(" ")[0] or "", name.split(" ")[1] or "")
    
    def create(self, validated_data: dict) -> User:
        image = validated_data.pop("image")
        validated_data["first_name"], validated_data["last_name"] = self.get_names_pair(validated_data.pop("name"))
        instance = super().create(validated_data)
        validated_data["password"] = get_random_string(32)
        Profile.objects.update_or_create(user=instance, defaults={"oauth_profile_image": image})
        return instance

class AdapterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "email_verified"]


class GetUserByIdSerializer(serializers.Serializer):
    id = serializers.CharField(required=True, write_only=True)


class GetUserByEmailPayloadSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

class DeleteUserPayloadSerializer(serializers.Serializer):
    id = serializers.EmailField(required=True, write_only=True, source="userId")


class GetUserByAccountPayloadSerializer(serializers.Serializer):
    provider = serializers.CharField(required=True, write_only=True)
    provider_account_id = serializers.CharField(
        required=True, write_only=True, source="providerAccountId"
    )
    
    def retrieve(self, validated_data: dict) -> Account:
        provider = validated_data.get("provider")
        provider_account_id = validated_data.get("providerAccountId")
        return Account.objects.get(
            provider=provider, provider_account_id=provider_account_id
        )

class GetUserByAccountSerilizer(serializers.Serializer):
    provider = serializers.CharField(required=True, write_only=True)
    provider_account_id = serializers.CharField(
        required=True, write_only=True
    )
    
    class Meta:
        fields = '__all__'
    
    def retrieve(self, validated_data: dict) -> Account:
        provider = validated_data.get("provider")
        provider_account_id = validated_data.get("provider_account_id")
        return Account.objects.get(
            provider=provider, provider_account_id=provider_account_id
        )

class LinkAccountSerializer(serializers.ModelSerializer):
    providerAccountId = serializers.CharField(
        source="provider_account_id"
    )
    userId = serializers.CharField(source="user_id")
    class Meta:
        model = Account
        fields = [
            'id',
            'userId',
            'type',
            'provider',
            'providerAccountId',
            'refresh_token',
            'access_token',
            'expires_at',
            'token_type',
            'scope',
            'id_token',
            'session_state'
        ]
