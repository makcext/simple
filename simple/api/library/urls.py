from django.urls import path, re_path, include
from rest_framework import routers
from simple.api.library.views.root import AuthorListView

router = routers.DefaultRouter()

urlpatterns = [
    re_path(
        r"^author/$",
        AuthorListView.as_view(),
        name="author-list",
        ),
    re_path(r"", include(router.urls)),
]
