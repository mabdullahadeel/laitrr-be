from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.mixins import WrappedResponseMixin
from . import serializers


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
