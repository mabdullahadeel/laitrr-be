from django.conf import settings
from abc import ABC, abstractmethod
from urllib.parse import urlencode
from .serializers import (
    SocialAuthQueryParamValidationSerializer as SocialAuthSerializer,
)


class AllowedAuthProviders:
    GOOGLE_OAUTH2 = "google-oauth2"

    @classmethod
    def get_auth_providers(cls):
        return [
            cls.GOOGLE_OAUTH2,
        ]


class SocialAuthUrlGenerator(ABC):
    @abstractmethod
    def get_auth_url(self, serializer: SocialAuthSerializer) -> str:
        """Generate auth url for social auth

        Returns:
            str: auth url
        """
        pass


class GoogleOAuthUrl(SocialAuthUrlGenerator):
    def __init__(self) -> None:
        self.BASE_URL = "https://accounts.google.com/o/oauth2/auth"
        self.SOCIALACCOUNT_PROVIDERS = getattr(settings, "SOCIALACCOUNT_PROVIDERS", {})
        self.google_oauth_config = self.SOCIALACCOUNT_PROVIDERS.get("google", {}).get(
            "APP", {}
        )
        self.GOOGLE_OAUTH2_KEY = self.google_oauth_config.get("client_id")

    def get_encoded_params(self, serializer: SocialAuthSerializer) -> str:
        return urlencode(
            {
                "client_id": self.GOOGLE_OAUTH2_KEY,
                "redirect_uri": serializer.validated_data.get("redirect_url"),
                "response_type": "code",
                "scope": " ".join(self.google_oauth_config.get("scope", [])),
            }
        )

    def get_auth_url(self, serializer: SocialAuthSerializer) -> str:
        return f"{self.BASE_URL}?{self.get_encoded_params(serializer)}"
