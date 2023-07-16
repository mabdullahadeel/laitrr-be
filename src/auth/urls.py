from . import views
from django.urls import path
from dj_rest_auth.views import LogoutView

urlpatterns = [
    path("social/", views.SocialAuthView.as_view(), name="social_auth"),
    path("google/", views.GoogleLogin.as_view(), name="google_login"),
    path("refresh/", views.refresh_token, name="refresh_token"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("test/", views.test_view, name="test"),
]
