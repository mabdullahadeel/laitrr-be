from . import views
from django.urls import path

app_name = "events"

urlpatterns = [
    path("", views.EventsList.as_view(), name="events-list"),
    path("create/", views.EventCreate.as_view(), name="event-create"),
    path(
        "<uuid:event_id>/announcements/",
        views.EventAnnouncementList.as_view(),
        name="event-announcements-list",
    ),
    path(
        "<uuid:event_id>/announcements/create/",
        views.EventAnnouncementCreate.as_view(),
        name="event-announcement-create",
    ),
    path("<uuid:event_id>/update/", views.EventUpdate.as_view(), name="event-update"),
    path("<uuid:event_id>/delete/", views.EventDelete.as_view(), name="event-delete"),
    path("follow/", views.EventFollow.as_view(), name="event-follow"),
    path(
        "<uuid:event_id>/unfollow/",
        views.EventUnfollow.as_view(),
        name="event-unfollow",
    ),
    path("<uuid:event_id>/", views.EventDetail.as_view(), name="event-detail"),
    path("event-types/", views.EventTypeList.as_view(), name="event-types-list"),
]
