from django.urls import include, path, re_path
from rest_framework import routers

<<<<<<< HEAD
from simple.api.movies.views.root import MovieCategoryListView, MovieCategoryByIdView, NextActiveMovieView
=======
from simple.api.movies.views.root import MovieCategoryListView, MovieCategoryByIdView, GetActiveMovieView
>>>>>>> 2af5e960b44c9e5558a452b7de3c53d76e2e0290

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
<<<<<<< HEAD
        r"^movies/next-active/$",
        NextActiveMovieView.as_view(),
        name="next-active-movie",
=======
        r"^movies/active/$",
        GetActiveMovieView.as_view(),
        name="get-active-movie",
>>>>>>> 2af5e960b44c9e5558a452b7de3c53d76e2e0290
    ),
  re_path(r"", include(router.urls)),
]
