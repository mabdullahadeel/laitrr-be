from typing import Type
from django.db import models
from django.http import HttpRequest
from core.db import generate_db_id
from rest_framework import exceptions
from django.contrib.auth import get_user_model

from users.models import User as CustomUser, UserFollow
from django_stubs_ext.db.models import TypedModelMeta

User: Type[CustomUser] = get_user_model()


class EventType(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=generate_db_id)
    heading = models.CharField(max_length=255, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    DEFAULT_HEADING = "Other"

    @classmethod
    def default_event_type(cls):
        return cls.objects.get_or_create(heading=cls.DEFAULT_HEADING)[0]

    class Meta(TypedModelMeta):
        db_table = "event_types"
        verbose_name = "Event Type"
        verbose_name_plural = "Event Types"
        ordering = ["-create_at"]

    def __str__(self):
        return self.heading


class EventManager(models.Manager):
    def delete_event(self, request: HttpRequest, event_id: str) -> bool:
        event: Event = self.filter(id=event_id).first()
        if event is None:
            raise exceptions.NotFound({"event_id": "Event does not exist"})

        if event.owner != request.user:
            raise exceptions.PermissionDenied(
                {"message": "User is not the owner of the event"}
            )

        event.delete()
        return True


class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=generate_db_id)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="events")
    type = models.ForeignKey(
        to=EventType,
        related_name="events",
        on_delete=models.SET_DEFAULT,
        default=EventType.default_event_type,
    )
    resource_url = models.URLField(null=True, blank=True)
    start_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventManager()

    class Meta(TypedModelMeta):
        db_table = "events"
        ordering = ["-created_at"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title


class EventAnnouncement(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=generate_db_id)
    event = models.ForeignKey(
        to=Event, on_delete=models.CASCADE, related_name="announcements"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(TypedModelMeta):
        db_table = "event_announcements"
        verbose_name = "Event Announcement"
        verbose_name_plural = "Event Announcements"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class EventFollower(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=generate_db_id)
    event = models.ForeignKey(
        to=Event, on_delete=models.CASCADE, related_name="followers"
    )
    follower = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="event_following"
    )
    alert_preference = models.ForeignKey(
        to="EventAlertPreference",
        on_delete=models.CASCADE,
        related_name="event_followers",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(TypedModelMeta):
        db_table = "event_followers"
        ordering = ["created_at"]
        verbose_name = "Event Follower"
        verbose_name_plural = "Event Followers"

    def __str__(self):
        return f"{self.follower} --> {self.event}"


class EventAlertPreference(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=generate_db_id)
    event_types = models.ManyToManyField(
        to=EventType, related_name="event_alerts", blank=True
    )
    all_events = models.BooleanField(default=False)
    user_follow = models.ForeignKey(
        to=UserFollow,
        on_delete=models.CASCADE,
        related_name="event_alerts",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(TypedModelMeta):
        db_table = "event_alert_preferences"
        verbose_name = "Event Alert Preference"
        verbose_name_plural = "Event Alert Preferences"
        ordering = ["-created_at"]

    def __str__(self):
        return self.id
