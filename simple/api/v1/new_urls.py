from django.urls import path
from simple.api.v1.views.new_views import MovieListAPIView, AuthorCreateAPIView, BookCreateAPIView
urlpatterns = [

    path('movies/', MovieListAPIView.as_view(), name='movie-list'),

    path('authors/', AuthorCreateAPIView.as_view(), name='author-create'),

    path('books/', BookCreateAPIView.as_view(), name='book-create'),
]
