from django.urls import re_path, include
from rest_framework import routers
from simple.api.library.views.root import (
    AuthorListView,
    AuthorByIdView,
    AuthorBooksView,
)

router = routers.DefaultRouter()

urlpatterns = [
    re_path(r"^author/$", AuthorListView.as_view(), name="author-list"),
    re_path(r"^author/(?P<id>\d+)/$", AuthorByIdView.as_view(), name="author-detail"),
    re_path(
        r"^author/(?P<author_id>\d+)/books/$",
        AuthorBooksView.as_view(),
        name="author-books",
    ),
    re_path(r"", include(router.urls)),
]
