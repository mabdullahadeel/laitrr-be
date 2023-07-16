from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("follow/", views.FollowUser.as_view(), name="follow"),
    path("unfollow/", views.UnFollowUser.as_view(), name="unfollow"),
]
