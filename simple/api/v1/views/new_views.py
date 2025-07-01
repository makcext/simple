from rest_framework import generics
from simple.models.models import Movie, Author, Book
from simple.api.v1.serializers.new_serializers import MovieSerializer, AuthorSerializer, BookSerializer


class MovieListAPIView(generics.ListAPIView):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class AuthorCreateAPIView(generics.CreateAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookCreateAPIView(generics.CreateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
