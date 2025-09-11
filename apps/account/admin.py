from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from apps.account.models import User, UserProfile, UserAddress
from utils.bases.base_admin import BaseAdmin


@admin.register(User)
class UserAdmin(DjangoUserAdmin, BaseAdmin):
    list_display = (
        "username",
        "phone_number",
        "email",
        "is_staff",
        "is_deleted",
        "deleted_at",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "is_deleted", "deleted_at")
    search_fields = ("username", "email", "phone_number", "id")
    date_hierarchy = "date_joined"
    actions = ["soft_delete_selected", "soft_undelete_selected"]

    readonly_fields = ("last_login", "date_joined", "deleted_at")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
        ("Soft Delete", {"fields": ("is_deleted", "deleted_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "phone_number",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj:
            readonly_fields.append("password")
        return readonly_fields


@admin.register(UserProfile)
class UserProfileAdmin(BaseAdmin):
    list_display = ("user", "is_active", "is_verified", "verified_by")
    list_filter = ("is_active", "is_verified", "verified_by")
    search_fields = ("user__phone_number", "user__first_name", "user__last_name", "id")
    actions = ["soft_delete_selected", "soft_undelete_selected"]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ("user",)
        return readonly_fields


@admin.register(UserAddress)
class UserAddressAdmin(BaseAdmin):
    list_display = (
        "user",
        "country",
        "province",
        "city",
        "is_active",
        "is_verified",
        "verified_by",
    )
    list_filter = (
        "is_active",
        "is_verified",
        "verified_by",
        "country",
        "province",
        "city",
    )
    search_fields = (
        "user__phone_number",
        "user__first_name",
        "user__last_name",
        "id",
        "country",
        "province",
        "city",
        "postal_code",
    )
    actions = ["soft_delete_selected", "soft_undelete_selected"]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ("user",)
        return readonly_fields
