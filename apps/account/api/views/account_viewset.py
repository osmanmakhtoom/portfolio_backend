from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.account.models import User
from apps.account.api.v1.serializers import (
    UserSerializerV1,
    UserProfileSerializerV1,
    UserAddressesSerializerV1,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializerV1
    lookup_field = "id"
    http_method_names = ["get", "post", "delete", "patch", "put"]

    def get_serializer_class(self):
        if self.request.version == "v1":
            return UserSerializerV1
        return super().get_serializer_class()

    def get_view_name(self):
        return "Users"

    def get_view_description(self, html=False):
        return "Account and Users Actions"

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'destroy', 'reset_password']:
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ['me', 'add_address', 'edit_profile']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'register':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [perm() for perm in permission_classes]

    @swagger_auto_schema(tags=["Users"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Users"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method="get",
        operation_description="Get current logged-in user's info.",
        responses={200: UserSerializerV1},
        tags=["Users"],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="me",
    )
    def me(self, request):
        return Response(self.get_serializer(request.user).data)

    @swagger_auto_schema(
        method="post",
        operation_description="Register a new user.",
        request_body=UserSerializerV1,
        responses={201: UserSerializerV1},
        tags=["Users"],
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="register",
    )
    def register(self, request):
        data = request.data.copy()
        data["password"] = make_password(data.get("password"))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(self.get_serializer(user).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method="post",
        operation_description="Reset password for a user (admin only).",
        manual_parameters=[
            openapi.Parameter(
                "user_id", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["new_password"],
            properties={
                "new_password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        tags=["Users"],
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="reset-password",
    )
    def reset_password(self, request):
        user_id = request.query_params.get("user_id")
        new_password = request.data.get("new_password")

        if not user_id or not new_password:
            return Response(
                {"detail": "user_id and new_password are required."}, status=400
            )

        try:
            user = User.objects.get(id=user_id)
            user.password = make_password(new_password)
            user.save()
            return Response({"detail": "Password reset successfully."}, status=200)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

    @swagger_auto_schema(
        method="post",
        tags=["Users"],
        request_body=UserAddressesSerializerV1,
        operation_summary="Add address to current user",
        responses={201: UserAddressesSerializerV1()},
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="add-address",
    )
    def add_address(self, request):
        serializer = UserAddressesSerializerV1(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.save(user=request.user)
        return Response(
            UserAddressesSerializerV1(address).data, status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def partial_update(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @swagger_auto_schema(
        method="patch",
        tags=["Users"],
        request_body=UserProfileSerializerV1,
        operation_summary="Edit current user's profile",
        responses={200: UserProfileSerializerV1()},
    )
    @action(
        detail=False,
        methods=["patch"],
        url_path="edit-profile",
    )
    def edit_profile(self, request):
        profile = request.user.userprofile
        serializer = UserProfileSerializerV1(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
