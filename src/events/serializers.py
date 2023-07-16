from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from users.serializers import UserPublicSerializer
from .models import (
    Event,
    EventAlertPreference,
    EventAnnouncement,
    EventType,
    EventFollower,
)


class EventSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer()

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]


class EventDetailsSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer()
    user_following_event = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"
        depth = 1

    def get_user_following_event(self, obj):
        user = self.context["request"].user
        return EventFollower.objects.filter(event=obj, follower=user).exists()


class EventCreateSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=EventType.objects.all(),
    )
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Event
        fields = "__all__"
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def create(self, validated_data: dict):
        validated_data.setdefault("type", EventType.default_event_type())
        return super().create(validated_data)


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
        ]

    def update(self, instance: Event, validated_data: dict):
        if serializers.CurrentUserDefault() != instance.owner:
            raise PermissionDenied({"message": "User is not the owner of the event"})

        return super().update(instance, validated_data)


class EventAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventAnnouncement
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "event",
            "created_at",
            "updated_at",
        ]


class EventAnnouncementCreateSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EventAnnouncement
        fields = ["title", "description", "event"]

    def create(self, validated_data):
        event = Event.objects.get(id=self.context["view"].kwargs["event_id"])
        validated_data["event"] = event

        if event.owner != self.context["request"].user:
            raise PermissionDenied({"message": "User is not the owner of the event"})

        return super().create(validated_data)


class FollowEventSerializer(serializers.Serializer):
    event_id = serializers.CharField(max_length=36)

    class Meta:
        fields = ["event_id"]

    def create(self, validated_data: dict):
        user = self.context["request"].user
        if EventFollower.objects.filter(
            event_id=validated_data["event_id"], follower=user
        ).exists():
            raise serializers.ValidationError({"message": "User already following"})

        if Event.objects.filter(id=validated_data["event_id"], owner=user).exists():
            raise serializers.ValidationError(
                {"message": "User cannot follow their own event"}
            )

        follow = EventFollower(follower=user, event_id=validated_data["event_id"])
        # check if user is following the owner of the event
        alert_preference = EventAlertPreference.objects.filter(
            user_follow__user=follow.event.owner, user_follow__follower=user
        )
        if alert_preference.exists():
            follow.alert_preference = alert_preference.first()
        follow.save()
        return follow


class ListEventTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = "__all__"
