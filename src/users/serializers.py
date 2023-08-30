from typing import Type
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserFollow, User as CustomUser, Profile

User: Type[CustomUser] = get_user_model()


class PublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ["user"]


class UserPublicSerializer(serializers.ModelSerializer):
    profile = PublicProfileSerializer()
    full_name = serializers.CharField(source="get_full_name", read_only=True)
    name_initials = serializers.SerializerMethodField(method_name="get_name_initials")
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "profile",
            "full_name",
            "name_initials"
        ]
        read_only_fields = ["profile"]
    
    def get_name_initials(self, obj):
        initials = ""
        if len(obj.first_name) > 0:
            initials += obj.first_name[0]
        if len(obj.last_name) > 0:
            initials += obj.last_name[0]
        if len(initials) == 0:
            initials = obj.username[0:2].upper()
        
        return initials


class FollowUserSerializer(serializers.Serializer):
    follower_id = serializers.CharField(max_length=36)

    class Meta:
        fields = [
            "follower_id",
        ]

    def validate_follower_id(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError(detail={"message": "User does not exist"})
        return value

    def create(self, validated_data):
        user: CustomUser = self.context["request"].user
        try:
            UserFollow.objects.get_or_create(
                user_id=validated_data["follower_id"], follower_id=user.id
            )
            return validated_data
        except Exception as e:
            raise serializers.ValidationError(detail={"message": str(e)})

    def delete(self, validated_data):
        user: CustomUser = self.context["request"].user
        try:
            r = UserFollow.objects.filter(
                user_id=validated_data["follower_id"], follower_id=user.id
            )
            print(validated_data)
            print(r)
            UserFollow.objects.filter(
                user_id=validated_data["follower_id"],
                follower_id=user.id,
            ).delete()
            return validated_data
        except Exception as e:
            raise serializers.ValidationError(detail={"message": str(e)})
