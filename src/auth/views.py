from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response as DRFResponse
from django.http import HttpRequest
from drf_spectacular.utils import extend_schema
from core.response import Response
from jwt import decode
from rest_framework_simplejwt.settings import api_settings as simplejwt_settings
from dj_rest_auth.jwt_auth import CookieTokenRefreshSerializer, set_jwt_access_cookie
from rest_framework.decorators import api_view, permission_classes

from users.models import User, Profile
from users.serializers import UserPublicSerializer
from .utils import AllowedAuthProviders, GoogleOAuthUrl
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from . import serializers as auth_serializers


class SocialAuthView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            auth_serializers.SocialAuthQueryParamValidationSerializer,
        ],
        request=None,
        responses={200: auth_serializers.SocialAuthResponseSerializer},
    )
    def get(self, request: HttpRequest):
        serializer = auth_serializers.SocialAuthQueryParamValidationSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

        provider = serializer.validated_data.get("provider")

        if provider == AllowedAuthProviders.GOOGLE_OAUTH2:
            url = GoogleOAuthUrl().get_auth_url(serializer)
            return Response.success(data={"authorization_url": url})

        return Response.error(error="Invalid payload")


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/auth/google/callback/"
    client_class = OAuth2Client
    permission_classes = [permissions.AllowAny]


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def refresh_token(request):
    d = CookieTokenRefreshSerializer(context={"request": request}).validate(
        request.data
    )
    token_payload = decode(
        d.get("access", None),
        verify=False,
        algorithms=[simplejwt_settings.ALGORITHM],
        key=simplejwt_settings.SIGNING_KEY,
    )
    user_id = token_payload.get("user_id", None)
    if not user_id:
        return Response.error(error={"message": "Invalid payload"})

    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response.error(error={"message": "Invalid payload"})
    serializer = UserPublicSerializer(user)
    d["user"] = serializer.data

    response = Response.success(data=d)
    set_jwt_access_cookie(response, d.get("access", None))
    return response


@api_view(["GET"])
def test_view(request):
    return Response.success(data={"message": "Hello World!"})


class SignupAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            auth_serializers.AdapterUserPayloadSerializer,
        ],
        request=None,
        responses={200: auth_serializers.AdapterUserSerializer},
    )
    def get(self, request: HttpRequest):
        serializer = auth_serializers.AdapterUserPayloadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

        user = User.objects.create(
            email=serializer.validated_data.get("email"),
            email_verified=serializer.validated_data.get("email_verified"),
        )
        user.set_password(get_random_string(32))
        profile_image = serializer.validated_data.get("image")
        user.save()
        if profile_image is not None:
            user.profile = Profile(profile_image=serializer.validated_data.get("image")).save()
        return DRFResponse(data=auth_serializers.AdapterUserSerializer(serializer.data).data, status=status.HTTP_201_CREATED)


class RetrieveUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            auth_serializers.AdapterUserPayloadSerializer,
        ],
        request=None,
        responses={200: auth_serializers.AdapterUserSerializer},
    )
    def get(self, request: HttpRequest):
        serializer = auth_serializers.GetUserByIdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

        user = User.objects.filter(id=serializer.validated_data.get("id")).first()
        
        if user is None:
            return Response.error(error={"message": "User not found"})
        
        return DRFResponse(data=auth_serializers.AdapterUserSerializer(user).data, status=status.HTTP_200_OK)


class RetrieveUserByEmailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            auth_serializers.AdapterUserPayloadSerializer,
        ],
        request=None,
        responses={200: auth_serializers.AdapterUserSerializer},
    )
    def get(self, request: HttpRequest):
        serializer = auth_serializers.AdapterUserPayloadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

        user = User.objects.filter(email=serializer.validated_data.get("email")).first()
        
        if user is None:
            return Response.error(error={"message": "User not found"})
        
        return DRFResponse(data=auth_serializers.AdapterUserSerializer(user).data, status=status.HTTP_200_OK)


class RetrieveUserByAccountAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            auth_serializers.GetUserByAccountSerilizer,
        ],
        request=None,
        responses={200: auth_serializers.AdapterUserSerializer},
    )
    def get(self, request: HttpRequest):
        serializer = auth_serializers.GetUserByAccountSerilizer(data=request.data)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

        user = User.objects.filter(accounts__id=serializer.validated_data.get("id")).first()
        
        return DRFResponse(data=auth_serializers.AdapterUserSerializer(user).data, status=status.HTTP_200_OK)


class UpdateUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            auth_serializers.AdapterUserPayloadSerializer,
        ],
        request=None,
        responses={200: auth_serializers.AdapterUserSerializer},
    )
    def put(self, request: HttpRequest):
        serializer = auth_serializers.AdapterUserPayloadSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

        user = User.objects.filter(email=serializer.validated_data.get("email")).first()
        
        if user is None:
            return Response.error(error={"message": "User not found"})
        
        if serializer.validated_data.get("name") is not None:
          user.first_name = serializer.validated_data.get("name")
        if serializer.validated_data.get("email") is not None:
          user.email = serializer.validated_data.get("email")
        if serializer.validated_data.get("email_verified") is not None:
          user.email_verified = serializer.validated_data.get("email_verified")
        if serializer.validated_data.get("image") is not None:
          user.profile.profile_image = serializer.validated_data.get("image")
          user.profile.save()
        user.save()
        return DRFResponse(data=auth_serializers.AdapterUserSerializer(user).data, status=status.HTTP_200_OK)