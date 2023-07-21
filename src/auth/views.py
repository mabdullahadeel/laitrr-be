from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from django.http import HttpRequest
from core.response import Response

from users.models import User
from . import serializers as auth_serializers

class SignupAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest):
        serializer = auth_serializers.AdapterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )
        serializer.save()
        return Response.success(
            data=auth_serializers.AdapterUserSerializer(serializer.data).data,
            status=status.HTTP_201_CREATED,
        )


class RetrieveUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest):
        serializer = auth_serializers.GetUserByIdSerializer(data=request.data)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_200_OK,
            )

        user = User.objects.filter(id=serializer.validated_data.get("id")).first()

        if user is None:
            return Response.error(error={"message": "User not found"})

        return Response.success(
            data=auth_serializers.AdapterUserSerializer(user).data,
            status=status.HTTP_200_OK,
        )


class RetrieveUserByEmailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest):
        serializer = auth_serializers.GetUserByEmailPayloadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )

        user = User.objects.filter(email=serializer.validated_data.get("email")).first()

        if user is None:
            return Response.error(error={"message": "User not found"}, status=status.HTTP_200_OK)

        return Response.success(
            data=auth_serializers.AdapterUserSerializer(user).data,
            status=status.HTTP_200_OK,
        )


class RetrieveUserByAccountAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = auth_serializers.GetUserByAccountSerilizer
    
    def post(self, request: HttpRequest):
        serializer = auth_serializers.GetUserByAccountSerilizer(data=request.data)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_200_OK,
                error=serializer.errors,
            )
        
        try:
          account = serializer.retrieve(serializer.validated_data)
        except Exception as e:
          return Response.error(status=status.HTTP_200_OK)

        return Response.success(
            data=auth_serializers.AdapterUserSerializer(account.user).data,
            status=status.HTTP_200_OK,
        )


class UpdateUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request: HttpRequest):
        serializer = auth_serializers.AdapterUserSerializer(
            data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_200_OK,
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
        return Response.success(
            data=auth_serializers.AdapterUserSerializer(user).data,
            status=status.HTTP_200_OK,
        )


class DeletUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest):
        serializer = auth_serializers.DeleteUserPayloadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response.error(
                status=status.HTTP_400_BAD_REQUEST,
                error=serializer.errors,
            )
        user = User.objects.filter(id=serializer.validated_data.get("id")).first()
        if user is None:
            return Response.error(error={"message": "User not found"})
        user.delete()
        return Response.success(
            data=auth_serializers.AdapterUserSerializer(user).data,
            status=status.HTTP_200_OK,
        )


class LinkAccountAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: HttpRequest):
        serialize = auth_serializers.LinkAccountSerializer(data=request.data)
        if not serialize.is_valid():
            print(serialize.errors)
            return Response.error(
                status=status.HTTP_400_BAD_REQUEST,
                error=serialize.errors,
            )
        try:
            serialize.create(serialize.validated_data)
            return Response.success(data=serialize.data)
        except Exception as e:
            print(e)
            return Response.error(error=str(e))
