from . import views
from django.urls import path

urlpatterns = [
    # next auth http adapter custom methods
    path("signup/", views.SignupAPIView.as_view(), name="signup"),
    path("get-user/", views.RetrieveUserAPIView.as_view(), name="get_user"),
    path("get-user-by-email/", views.RetrieveUserByEmailAPIView.as_view(), name="get_user_by_email"),
    path("get-user-by-account/", views.RetrieveUserByAccountAPIView.as_view(), name="get_user_by_account"),
    path("update-user/", views.UpdateUserAPIView.as_view(), name="update_user"),
    path("delete-user/", views.DeletUserAPIView.as_view(), name="delete_user"),
    path("link-account/", views.LinkAccountAPIView.as_view(), name="link_account"),
    # path("unlink-account/", views.unlink_account, name="unlink_account"),
    # path("create-session/", views.create_session, name="create_session"),
    # path("get-session-and-user/", views.get_session_and_user, name="get_session_and_user"),
    # path("update-session/", views.update_session, name="update_session"),
    # path("delete-session/", views.delete_session, name="delete_session"),
    # path("create-verification-token/", views.create_verification_token, name="create_verification_token"),
    # path("use-verification-token/", views.use_verification_token, name="use_verification_token"),
]
