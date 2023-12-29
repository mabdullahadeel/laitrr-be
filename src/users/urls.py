from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("follow/", views.FollowUser.as_view(), name="follow"),
    path("unfollow/", views.UnFollowUser.as_view(), name="unfollow"),
    path("signin/", views.SignIn.as_view(), name="signin"),
    path("get-public-profile/<str:username>/", views.UserPublicProfile.as_view(), name="get-public-profile"),
]
