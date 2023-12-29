from . import views
from django.urls import path

app_name = "events"

urlpatterns = [
    path("feed/", views.EventsList.as_view(), name="events-list"),
    path("create/", views.EventCreate.as_view(), name="event-create"),
    path("follow/", views.EventFollow.as_view(), name="event-follow"),
    path("event-types/", views.EventTypeList.as_view(), name="event-types-list"),
    path("update/<uuid:id>/", views.EventUpdate.as_view(), name="event-update"),
    path("delete/<uuid:event_id>/", views.EventDelete.as_view(), name="event-delete"),
    path(
        "unfollow/<uuid:event_id>/",
        views.EventUnfollow.as_view(),
        name="event-unfollow",
    ),
    path("details/<uuid:event_id>/", views.EventDetail.as_view(), name="event-detail"),
    path(
        "event-announcements/<uuid:event_id>/",
        views.EventAnnouncementList.as_view(),
        name="event-announcements-list",
    ),
    path(
        "announcements/create/<uuid:event_id>/",
        views.EventAnnouncementCreate.as_view(),
        name="event-announcement-create",
    ),
    path(
        "announcements/update/<uuid:announcement_id>/",
        views.EventAnnouncementUpdate.as_view(),
        name="event-announcement-update",
    ),
    path(
        "announcements/delete/<uuid:announcement_id>/",
        views.EventAnnouncementDelete.as_view(),
        name="event-announcement-delete",
    ),
    path(
        "announcements/<uuid:announcement_id>/",
        views.EventAnnouncementDetail.as_view(),
        name="event-announcement-detail",
    ),
    path("user/<str:username>/", views.UserEventsList.as_view(), name="user-events-list"),
]
