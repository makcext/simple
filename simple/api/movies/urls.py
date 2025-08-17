from django.urls import include, path, re_path
from rest_framework import routers

from simple.api.movies.views.root import MovieCategoryListView, MovieCategoryByIdView, GetActiveMovieView

router = routers.DefaultRouter()

urlpatterns = [
  re_path(
    r"^movies-category/$",
    MovieCategoryListView.as_view(),
    name="movie-category-list",
  ),
  re_path(
        r"^movies-category/(?P<id>\d+)/$",
        MovieCategoryByIdView.as_view(),
        name="movie-category-detail",
    ),
  re_path(
        r"^movies/active/$",
        GetActiveMovieView.as_view(),
        name="get-active-movie",
    ),
  re_path(r"", include(router.urls)),
]
