from django.urls import path
from .views.root import MovieCategoryListView, MovieCategoryByIdView

urlpatterns = [
    path('movies-category/', MovieCategoryListView.as_view(), name='movie-category-list'),
    path('movies-category/<int:id>/', MovieCategoryByIdView.as_view(), name='movie-category-detail'),
]
