from . import views
from django.urls import path
from dj_rest_auth.views import LogoutView

urlpatterns = [
    path("social/", views.SocialAuthView.as_view(), name="social_auth"),
    path("google/", views.GoogleLogin.as_view(), name="google_login"),
    path("refresh/", views.refresh_token, name="refresh_token"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("test/", views.test_view, name="test"),
    # next auth http adapter custom methods
    # path("signup/", views.signup, name="signup"),
    # path("get-user/", views.get_user, name="get_user"),
    # path("get-user-by-email/", views.get_user, name="get_user_by_email"),
    # path("get-user-by-account/", views.get_user, name="get_user_by_account"),
    # path("update-user/", views.update_user, name="update_user"),
    # path("delete-user/", views.delete_user, name="delete_user"),
    # path("link-account/", views.link_account, name="link_account"),
    # path("unlink-account/", views.unlink_account, name="unlink_account"),
    # path("create-session/", views.create_session, name="create_session"),
    # path("get-session-and-user/", views.get_session_and_user, name="get_session_and_user"),
    # path("update-session/", views.update_session, name="update_session"),
    # path("delete-session/", views.delete_session, name="delete_session"),
    # path("create-verification-token/", views.create_verification_token, name="create_verification_token"),
    # path("use-verification-token/", views.use_verification_token, name="use_verification_token"),
]
