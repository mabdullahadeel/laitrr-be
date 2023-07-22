from django.utils.crypto import get_random_string
from rest_framework import serializers

from auth.models import Account, Session, VerficationToken
from users.models import User, Profile

class AdapterUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, allow_null=True)
    image = serializers.URLField(required=False, allow_null=True)
    emailVerified = serializers.DateTimeField(required=False, allow_null=True, source="email_verified")
    
    class Meta:
        model = User
        fields = ["id", "email", "emailVerified", "name", "image"]
        
    def get_names_pair(self, name: str) -> tuple[str, str]:
        name = name.split(" ")
        if len(name) == 2:
            return (name[0], name[1])
        elif len(name) == 1:
            return (name[0], "")
        else:
            return ("", "")
    
    def create(self, validated_data: dict) -> User:
        image = validated_data.pop("image", None)
        name = validated_data.pop("name", None)
        if name is not None:
            validated_data["first_name"], validated_data["last_name"] = self.get_names_pair(name)
            
        instance = super().create(validated_data)
        if name is not None:
            instance.name = validated_data.get("name")
        
        validated_data["password"] = get_random_string(32)
        if image is not None:
            Profile.objects.update_or_create(user=instance, defaults={"oauth_profile_image": image})
            instance.image = image
            
        return instance
    
    def update(self, instance: User, validated_data):
        if validated_data.get("name", None) is None:
            instance.name = instance.get_full_name()
        else:
            validated_data["first_name"], validated_data["last_name"] = self.get_names_pair(validated_data.get("name"))
        if validated_data.get("image", None) is None:
            instance.image = instance.profile.profile_image or instance.profile.oauth_profile_image or None
        return super().update(instance, validated_data)


class AdapterPublicUserSerializer(AdapterUserSerializer):
    name = serializers.CharField(source="get_full_name")
    image = serializers.SerializerMethodField()
    emailVerified = serializers.CharField(source="email_verified")

    def get_image(self, obj: User) -> str:
        return obj.profile.profile_image or obj.profile.oauth_profile_image or None
        
    class Meta:
        model = User
        fields = ["id", "email", "emailVerified", "name", "image"]


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


class RemoteAdapterSessionSerializer(serializers.ModelSerializer):
    sessionToken = serializers.CharField(source="session_token")
    userId = serializers.CharField(source="user_id")
    class Meta:
        model = Session
        fields = [
            'id',
            'userId',
            'sessionToken',
            'expires',
        ]

class RemoteAdapterSessionAndUserSerializer(serializers.Serializer):
    session = RemoteAdapterSessionSerializer()
    user = AdapterPublicUserSerializer()


class RemoteAdapterVerificationTokensSerializers(serializers.ModelSerializer):
    class Meta:
        model = VerficationToken
        fields = '__all__'