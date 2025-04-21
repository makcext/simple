"""
URL configuration for simple project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin

from django.urls import include, path

# from django.urls import re_path
# from drf_spectacular.views import (
#     SpectacularJSONAPIView,
#     SpectacularSwaggerView,
#     SpectacularRedocView,
# )
from rest_framework import routers
from drf_yasg.generators import OpenAPISchemaGenerator


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(SchemaGenerator, self).get_schema(request, public)
        schema.schemes = (
            ["http", "https"] if settings.ENV == "development" else ["https"]
        )

        return schema


router = routers.DefaultRouter()

# jwt_urlpatterns = [
#     re_path(
#         r"api/v1/",
#         include(
#             ("simple.api.v1.urls", "simple.api.v1"),
#             namespace="simple-api-v1",
#         ),
#     )
# ]

# swager_urlpatterns = [
#     path("api/v1/schema.json", SpectacularJSONAPIView.as_view(), name="spec-schema"),
#     path(
#         "api/v1/swagger/",
#         SpectacularSwaggerView.as_view(url_name="spec-schema"),
#         name="spec-swagger",
#     ),
#     path(
#         "api/v1/redoc/",
#         SpectacularRedocView.as_view(url_name="spec-schema"),
#         name="spec-redoc",
#     ),
# ]

urlpatterns = (
    [
        # Admin panel
        path("admin/", admin.site.urls),
        path("admin/autocomplete/", admin.site.autocomplete_view, name="autocomplete"),
        path("logs/", include("log_viewer.urls")),
        # Django Debug Toolbar
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    # + jwt_urlpatterns
    # + swager_urlpatterns
)
