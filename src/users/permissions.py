from django.conf import settings

from rest_framework.permissions import BasePermission

class AllowRemoteAuthServer(BasePermission):
    """
    Allow remote auth server to access this API.
    """

    def has_permission(self, request, view):
        token = request.META.get("HTTP_AUTHORIZATION", None)
        if token is None:
            return False

        if token != settings.REMOTE_AUTH_TOKEN:
            return False

        return True