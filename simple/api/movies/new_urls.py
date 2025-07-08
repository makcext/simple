from .views import MovieCategoryHandler, MovieCategoryByIdHandler

urlpatterns = [
    path(
        "movies-category/",
        MovieCategoryHandler.as_view(),
        name="movie-category-handler",
    ),
    path(
        "movies-category/<int:id>/",
        MovieCategoryByIdHandler.as_view(),
        name="movie-category-by-id-handler",
    ),
]
