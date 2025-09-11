from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view_v1 = get_schema_view(
    openapi.Info(
        title="Osman's Portfolio API",
        default_version="v1",
        description="The backend project of Osman's portfolio",
        contact=openapi.Contact(email="osmanmakhtoom@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

v1_patterns = [
    path(
        "account/",
        include("apps.account.api.v1.urls"),
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger.<format>/v1/", schema_view_v1.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/v1/",
        schema_view_v1.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/v1/", schema_view_v1.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/v1/", include((v1_patterns, "v1"))),
]

schema_view_v1._urlpatterns = v1_patterns
