from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .permissions import AllowRemoteAuthServer

from core.mixins import WrappedResponseMixin
from . import serializers
from .models import Profile, User as UserModel

User: UserModel = get_user_model()


class FollowUser(WrappedResponseMixin, generics.CreateAPIView):
    serializer_class = serializers.FollowUserSerializer


class UnFollowUser(WrappedResponseMixin, APIView):
    serializer_class = serializers.FollowUserSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.delete(serializer.data)
            return Response(
                {"message": "User unfollowed successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "User not unfollowed successfully"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SignIn(WrappedResponseMixin, APIView):
    permission_classes = [AllowRemoteAuthServer]

    def post(self, request):
        user_data = request.data.get("user")
        user = User.objects.filter(email=user_data.get("email")).first()
        
        if user:
            return Response(data=user.id, status=status.HTTP_200_OK)
        
        first_name, last_name = user_data.get("name").split(" ")
        user = User.objects.create(
            id=user_data.get("id"),
            email=user_data.get("email"),
            first_name=first_name,
            last_name=last_name,
            email_verified=user_data.get("emailVerified"),
        )
        profile, _ = Profile.objects.get_or_create(
            user=user,
        )
        profile.oauth_profile_image = user_data.get("image")
        profile.save()
        
        return Response(data=user.id, status=status.HTTP_201_CREATED)


class UserPublicProfile(WrappedResponseMixin, generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserPublicProfileSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    lookup_url_kwarg = "username"
