from django.contrib import admin
from .models import (
    Event,
    EventAnnouncement,
    EventType,
    EventFollower,
    EventAlertPreference,
)


class EventAnnouncementInline(admin.TabularInline):
    model = EventAnnouncement
    extra = 0


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "owner",
        "type",
        "created_at",
        "updated_at",
    )
    list_filter = ("type",)
    search_fields = ("title", "owner")
    readonly_fields = ("id", "created_at", "updated_at")

    inlines = [
        EventAnnouncementInline,
    ]


admin.site.register(Event, EventAdmin)
admin.site.register(EventType)
admin.site.register(EventAnnouncement)
admin.site.register(EventFollower)
admin.site.register(EventAlertPreference)
