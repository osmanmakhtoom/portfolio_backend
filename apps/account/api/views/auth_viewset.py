from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
    TokenBlacklistSerializer,
)


from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class TokenViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        method="post",
        request_body=TokenObtainPairSerializer,
        responses={200: TokenRefreshSerializer},
        operation_id="TokenObtainPair",
        operation_description="Obtain JWT access and refresh token.",
        tags=["Authentication"],
    )
    @action(detail=False, methods=["post"], url_path="obtain")
    def obtain(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=TokenRefreshSerializer,
        operation_id="TokenRefresh",
        operation_description="Refresh access token.",
        tags=["Authentication"],
    )
    @action(detail=False, methods=["post"], url_path="refresh")
    def refresh(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=TokenVerifySerializer,
        operation_id="TokenVerify",
        operation_description="Verify token validity.",
        tags=["Authentication"],
    )
    @action(detail=False, methods=["post"], url_path="verify")
    def verify(self, request):
        serializer = TokenVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Token is valid."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=TokenBlacklistSerializer,
        operation_id="TokenBlacklist",
        operation_description="Blacklist a refresh token.",
        tags=["Authentication"],
    )
    @action(detail=False, methods=["post"], url_path="blacklist")
    def blacklist(self, request):
        serializer = TokenBlacklistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Token blacklisted."}, status=status.HTTP_200_OK)
