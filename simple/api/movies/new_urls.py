from django.urls import path, re_path, include
from rest_framework import routers
from simple.api.movies.new_views import MovieCategory

router = routers.DefaultRouter()

urlpatterns = [
    re_path(
        r"^movies/$",
        .as_view(),
        name="movie-category-list",
        ),
    re_path(
        r"^movies/(?P<id>\d+)/$",
        AuthorListView.as_view(),
        name="movie-category-detail",
    ),
    re_path(r"", include(router.urls)),
]
