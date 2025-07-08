from django.urls import path, re_path, include
from rest_framework import routers
from simple.api.library.views import AuthorListView

router = routers.DefaultRouter()

urlpatterns = [
    re_path(
        r"^author/$",
        AuthorListView.as_view(),
        name="author-list",
        ),
    re_path(
        r"^author/(?P<id>\d+)/$",
        AuthorListView.as_view(),
        name="author-detail",
    ),
    re_path(r"", include(router.urls)),
]
